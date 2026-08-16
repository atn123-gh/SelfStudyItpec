import csv
import os
import django
import re
import time
from dotenv import load_dotenv
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from quiz.models.nosql_models import IPQuestion, FEQuestion
from itp_project.settings.mongodb_service import MongoDBService
from django.core.management.base import BaseCommand
import openai

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itp_project.settings')
django.setup()

# Base image URL (modify as needed)
BASE_IMAGE_URL = "https://raw.githubusercontent.com/yt2122/itpec_image/main/IP_FE_QImg_V1"

load_dotenv()  # Load environment variables from .env file
openai_api_key = os.getenv("OPENAI_API_KEY")

LOG_FILENAME = "update_log.csv"
LAST_PROCESSED_FILE = "last_processed_folder.csv"

def load_processed_status():
    """
    Loads a CSV file of the form:
      folder,question_id,status
      folder1,Q1,done
      folder1,Q2,pending
      folder2,Q5,done
    """
    if not os.path.exists(LAST_PROCESSED_FILE):
        return {}
    with open(LAST_PROCESSED_FILE, mode="r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        status_data = {}
        for row in reader:
            folder = row["folder"]
            question_id = row["question_id"]
            status = row["status"]
            if folder not in status_data:
                status_data[folder] = {}
            status_data[folder][question_id] = status
        return status_data

def save_processed_status(status_data):
    """
    Writes the current status to a CSV file.
    """
    with open(LAST_PROCESSED_FILE, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["folder", "question_id", "status"])
        writer.writeheader()
        for folder, questions in status_data.items():
            for question_id, status in questions.items():
                writer.writerow({"folder": folder, "question_id": question_id, "status": status})

def log_update(folder, question_id, correct_option):
    file_exists = os.path.isfile(LOG_FILENAME)
    with open(LOG_FILENAME, mode="a", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Folder", "QuestionID", "CorrectAnswer"])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "Folder": folder,
            "QuestionID": question_id,
            "CorrectAnswer": correct_option
        })

def process_questions(model, level):
    # Adjust BASE_IMAGE_URL based on the level
    if level == "IP":
        base_url = f"{BASE_IMAGE_URL}/IP/"
        collection_name = "ip_questions"
    elif level == "FE":
        base_url = f"{BASE_IMAGE_URL}/FE/"
        collection_name = "fe_questions"
    else:
        return

    # Get the collection
    collection = MongoDBService.get_collection(collection_name)
    questions = collection.find().sort("folder", 1)  # A-Z order
    total_folders = collection.count_documents({})
    processed_folders = 0
    
    # Load the external tracking info
    status_data = load_processed_status()

    for doc in questions:
        folder = doc['folder']
        folder_status = status_data.get(folder, {})

        print(f"Processing folder: {folder}")
        updated_solutions = {}
        updated_correct_options = {}

        for questionId, img_path in doc['questions'].items():
            if folder_status.get(questionId) == "done":
                print(f"Skipping question {questionId}: already marked done.")
                continue

            full_img_url = f"{base_url}{folder}/{img_path}"
            print(f"Processing question {questionId} in folder {folder}")
            correct_option, solution = get_openai_solution_and_choice(full_img_url)

            if correct_option and solution:
                updated_correct_options[questionId] = correct_option
                updated_solutions[questionId] = solution
                log_update(folder, questionId, correct_option)
                folder_status[questionId] = "done"

        if updated_solutions:
            update_fields = {}
            for question_id in updated_solutions:
                update_fields[f"solutions.{question_id}"] = updated_solutions[question_id]
                update_fields[f"correct_options.{question_id}"] = updated_correct_options[question_id]

            collection.update_one(
                {"_id": doc["_id"]},
                {"$set": update_fields}
            )
            print(f"Updated folder {folder}")

        status_data[folder] = folder_status
        save_processed_status(status_data)

        processed_folders += 1
        print(f"Progress: {processed_folders}/{total_folders} folders processed.")
        input("Press Enter to continue...")

    print("✅ Processing complete.")

def get_openai_solution_and_choice(image_url):
    return "Z", "dummy solution 03092025_0157"

def get_openai_solution_and_choiceII(image_url):
    client = openai.OpenAI(api_key=openai_api_key)
    correct_choice = None
    solution_text = None

    try:
        print("Sending request to OpenAI API...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI that provides detailed solutions for ITPEC IP and FE morning exam questions from an image."
                        " The question is provided as an image. Your response must strictly follow this format:"
                        "\n\nCorrect Answer: [a/b/c/d]\n\n"
                        "[Provide a detailed solution in clear, structured text or HTML snippet]"
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Please analyze this image and provide the correct answer choice (a, b, c, or d) "
                                "along with a detailed solution in the following format:\n\n"
                                "Correct Answer: a\n\n"
                                "<p>Explain the answer with HTML formatting.</p>\n\n"
                                "Make sure the answer format is exactly as shown above."
                            )
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        }
                    ],
                }
            ],
            max_tokens=600,  # Increased token limit for detailed answers
        )

        print("Request sent to OpenAI API")
        ai_response = response.choices[0].message.content
        print(ai_response)

        # Parse response
        correct_choice, solution_text = parse_ai_response(ai_response)

        if correct_choice and solution_text:
            return correct_choice, solution_text

    except Exception as e:
        print(f"Error: {e}")
        return "Error", "Error"

    return None, None  # Return None if no valid response

def parse_ai_response(ai_response):
    """
    Extracts the correct answer choice (a, b, c, or d) and solution from AI response.
    :param ai_response: String containing AI-generated solution and answer
    :return: Tuple (correct_choice, solution_text)
    """
    correct_choice = None
    solution_text = ai_response.strip()

    # Match "Correct Answer: a" (forcing lowercase letters only)
    match = re.search(r"Correct Answer:\s*([a-d])", solution_text)

    if match:
        correct_choice = match.group(1)  # Already lowercase
        # Remove the "Correct Answer" line from the solution text
        solution_text = re.sub(r"Correct Answer:\s*[a-d]", "", solution_text).strip()

    return correct_choice, solution_text

class Command(BaseCommand):
    def handle(self, *args, **options):
        process_questions(IPQuestion, "IP")
        # process_questions(FEQuestion, "FE")
