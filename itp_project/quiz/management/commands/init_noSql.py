from django.core.management.base import BaseCommand
from pymongo import MongoClient
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

class Command(BaseCommand):
    help = 'Insert IP and FE questions into MongoDB'

    def __init__(self):
        super().__init__()
        self.level = {"IP": 100, "FE": 80}

        self.Ipfoldername = [
            "2017S_IP_Question__2017_Apr",
            "2017A_IP_Question__2017_Oct",
            "2018S_IP_Question__2018_Mar",
            "2018A_IP_Question__2018_Oct",
            "2019S_IP_Question__2019_Apr",
            "2019A_IP_Question__2019_Oct",
            "2020S_IP_Question__2020_Q2",
            "2020A_IP_Question__2020_Oct",
            "2021A_IP_Question__2021_Q4",
            "2021S_IP_Question__2021_Q2",
            "2022S_IP_Question__2022_Apr",
            "2022A_IP_Question__2022_Oct",
        ]

        self.FEfoldername = [
            "2016S_FE_AM-Question__2016_Apr",
            "2007Apr_FE_AM_Questions__2007_Apr",
            "2007Oct_FE_AM_Questions__2007_Oct",
            "2008Apr_FE_AM_Questions__2008_Apr",
            "2008Oct_FE_AM_Questions__2008_Oct",
            "2009Apr_FE_AM_Questions__2009_Apr",
            "2009Oct_FE_AM_Questions__2009_Oct",
            "2010Apr_FE_AM_Questions__2010_Apr",
            "2010Oct_FE_AM_Questions__2010_Oct",
            "2011S_FE_AM_Questions__2011_Apr",
            "2011A_FE_AM_Question__2011_Oct",
            "2012S_FE_AM_Question__2012_Apr",
            "2012Oct_FE_AM_Question__2012_Oct",
            "2013Apr_FE_AM_Question__2013_Apr",
            "2013Oct_FE_AM_Question__2013_Oct",
            "2014S_FE_AM_Question__2014_Apr",
            "2014Oct_FE_AM_Question__2014_Oct",
            "2015May_FE_AM_Question__2015_May",
            "2015A_FE_AM_Question__2015_Oct",
            "2016A_FE_AM_Question__2016_Oct",
            "2017S_FE_AM_Question__2017_Apr",
            "2017A_FE_AM_Question__2017_Oct",
            "2018S_FE_AM_Question__2018_Mar",
            "2018A_FE_AM_Question__2018_Oct",
            "2019S_FE_AM_Question__2019_Apr",
            "2020A_FE_AM_Question__2020_Oct",
            "2021A_FE_AM_Questions__2021_Q4",
            "2021S_FE_AM_Question__2021_Q2",
            "2022S_FE_AM_Questions__2022_Apr",
            "2022A_FE_AM_Question__2022_Oct",
            "2020S_FE_AM_Question__2020_Q2",
            "2019A_FE_AM_Question__2019_Oct",
        ]

    def generate_questions_and_solutions(self, num_questions):
        questions = {f"Q{i+1}": f"Q{i+1}.png" for i in range(num_questions)}
        solutions = {f"Q{i+1}": f"dummy Q{i+1} solution" for i in range(num_questions)}
        correct_options = {f"Q{i+1}": 0 for i in range(num_questions)}
        ratings = {f"Q{i+1}": 0 for i in range(num_questions)}
        return questions, solutions, correct_options, ratings

    def insert_documents(self, db, collection_name, folder_list, level):
        collection = db[collection_name]

        inserted_count = 0
        for folder in folder_list:
            if not collection.find_one({"_id": folder}):  # Check if document exists
                questions, solutions, correct_options, ratings = self.generate_questions_and_solutions(level)
                collection.insert_one({
                    "_id": folder,  # Set folder as _id
                    "folder": folder,  # Still keep folder field
                    "questions": questions,
                    "solutions": solutions,
                    "correct_options": correct_options,
                    "ratings": ratings
                })
                inserted_count += 1

        return inserted_count

    def handle(self, *args, **options):
        try:
            # Load environment variables
            load_dotenv()

            # Get MongoDB settings from environment
            db_name = os.getenv('MONGO_DB_NAME', 'mongo_db')
            host = os.getenv('MONGO_DB_HOST', 'mongodb://mongodb:27017')
            username = quote_plus(os.getenv('MONGO_DB_USERNAME', 'root'))
            password = quote_plus(os.getenv('MONGO_DB_PASSWORD', 'example'))

            # Remove mongodb:// prefix if present
            host = host.replace('mongodb://', '')

            # Construct MongoDB URI
            uri = f"mongodb://{username}:{password}@{host}"

            # Connect to MongoDB
            with MongoClient(uri) as client:
                db = client[db_name]

                # Insert IP and FE questions
                ip_count = self.insert_documents(db, "ip_questions", self.Ipfoldername, self.level["IP"])
                fe_count = self.insert_documents(db, "fe_questions", self.FEfoldername, self.level["FE"])

                # Print the insertion summary
                self.stdout.write(self.style.SUCCESS(f"Inserted {ip_count} new IP documents"))
                self.stdout.write(self.style.SUCCESS(f"Inserted {fe_count} new FE documents"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {str(e)}"))
