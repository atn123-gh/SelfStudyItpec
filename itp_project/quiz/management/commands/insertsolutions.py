"""
Offline utility: generates AI explanations for exam questions and stores
them in MongoDB, for the website to later display as-is (no LLM calls at
runtime - see README).

Pipeline per question:
  1. Fetch the question image (from the external image host already used
     by the rest of the app).
  2. Gemini vision call: transcribe the image into question text + choices
     (the DB only stores an image filename per question, not text, so
     there's nothing to search with otherwise).
  3. Retrieve the top-k most relevant textbook chunks for that text (see
     _rag_retrieval.py - simple TF-IDF, no vector DB).
  4. Gemini text call: generate the HTML explanation fragment, grounded in
     the retrieved textbook context.
  5. Sanitize the HTML (bleach) and store it in the existing
     solutions.<QuestionId> / correct_options.<QuestionId> fields.

Usage:
  python manage.py insertsolutions --level FE --folder <folder_name> --limit 5
  python manage.py insertsolutions --level FE --folder <folder_name> --limit 5 --regenerate

Requires: pip install -r requirements/rag_utility.txt (not part of the
website's own requirements - see that file's header comment).
"""
import base64
import csv
import os
import re
import time

import bleach
import requests
from django.core.management.base import BaseCommand, CommandError

from itp_project.settings.mongodb_service import MongoDBService

from ._rag_retrieval import TextbookIndex

BASE_IMAGE_URL = "https://raw.githubusercontent.com/yt2122/itpec_image/main/IP_FE_QImg_V1"

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "insertsolutions_log.csv")

ALLOWED_TAGS = ["div", "h4", "h5", "p", "ul", "li", "strong", "em", "br"]
ALLOWED_ATTRIBUTES = {"div": ["class"]}

CHOICE_LETTERS = ["a", "b", "c", "d"]


class Command(BaseCommand):
    help = "Generate AI explanations for exam questions (offline utility, not run at request time)."

    def add_arguments(self, parser):
        parser.add_argument("--level", choices=["IP", "FE"], default="FE")
        parser.add_argument("--folder", required=True, help="Exact folder name to process, e.g. 2022A_FE_AM_Question__2022_Oct")
        parser.add_argument("--limit", type=int, default=5, help="Max questions to process from this folder")
        parser.add_argument("--regenerate", action="store_true", help="Regenerate even if a real explanation already exists")

    def handle(self, *args, **options):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise CommandError("GEMINI_API_KEY is not set - see .env.example")
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        level = options["level"]
        folder_name = options["folder"]
        limit = options["limit"]
        regenerate = options["regenerate"]

        collection_name = "ip_questions" if level == "IP" else "fe_questions"
        collection = MongoDBService.get_collection(collection_name)
        doc = collection.find_one({"folder": folder_name})
        if not doc:
            raise CommandError(f"No document found for folder '{folder_name}' in {collection_name}")

        self.stdout.write(f"Loading textbook index (first run builds+caches it, may take a moment)...")
        index = TextbookIndex()

        question_ids = sorted(doc["questions"].keys(), key=lambda q: int(q[1:]))[:limit]
        self.stdout.write(f"Processing {len(question_ids)} question(s) from {folder_name}: {question_ids}")

        log_rows = []

        for question_id in question_ids:
            existing = doc.get("solutions", {}).get(question_id, "")
            if existing and not existing.lower().startswith("dummy") and not regenerate:
                self.stdout.write(f"  {question_id}: already has a real explanation, skipping (use --regenerate to force)")
                log_rows.append([folder_name, question_id, "skipped", ""])
                continue

            try:
                img_filename = doc["questions"][question_id]
                image_url = f"{BASE_IMAGE_URL}/{level}/{folder_name}/{img_filename}"
                image_bytes = self._fetch_image(image_url)

                self.stdout.write(f"  {question_id}: transcribing question image...")
                transcript = self._transcribe_question(api_key, model, image_bytes)
                time.sleep(2)  # be gentle with free-tier rate limits

                self.stdout.write(f"  {question_id}: retrieving textbook context...")
                context_chunks = index.top_k(transcript, k=3)

                self.stdout.write(f"  {question_id}: generating explanation...")
                answer_letter, html = self._generate_explanation(api_key, model, transcript, context_chunks)
                time.sleep(2)

                clean_html = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)

                collection.update_one(
                    {"folder": folder_name},
                    {"$set": {
                        f"solutions.{question_id}": clean_html,
                        f"correct_options.{question_id}": answer_letter,
                    }},
                )
                self.stdout.write(self.style.SUCCESS(f"  {question_id}: saved (answer: {answer_letter})"))
                log_rows.append([folder_name, question_id, "success", ""])

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  {question_id}: FAILED - {e}"))
                log_rows.append([folder_name, question_id, "error", str(e)])

        self._append_log(log_rows)
        self.stdout.write(f"Done. Log: {LOG_PATH}")

    def _fetch_image(self, url: str) -> bytes:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        return resp.content

    def _call_gemini(self, api_key: str, model: str, parts: list) -> str:
        # Key goes in a header, not the URL query string - requests includes
        # the full URL (but not headers) in HTTPError messages, so a
        # ?key=... query param would otherwise leak into any error log.
        url = GEMINI_API_URL.format(model=model)
        headers = {"x-goog-api-key": api_key, "Content-Type": "application/json"}
        payload = {"contents": [{"parts": parts}]}

        last_error = None
        for attempt in range(4):
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            if resp.status_code in (429, 503):
                # Free-tier rate limiting / transient overload - retry with backoff.
                last_error = f"{resp.status_code} {resp.reason}"
                wait = 5 * (2 ** attempt)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

        raise RuntimeError(f"Gemini API unavailable after retries (last: {last_error})")

    def _transcribe_question(self, api_key: str, model: str, image_bytes: bytes) -> str:
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        prompt = (
            "Transcribe this exam question image into plain text. Output the question "
            "text, then each answer choice on its own line labeled a), b), c), d). "
            "Do not answer the question or explain anything - just transcribe it exactly."
        )
        return self._call_gemini(api_key, model, [
            {"text": prompt},
            {"inline_data": {"mime_type": "image/png", "data": image_b64}},
        ])

    def _generate_explanation(self, api_key: str, model: str, transcript: str, context_chunks: list[str]) -> tuple[str, str]:
        context_text = "\n\n---\n\n".join(context_chunks) if context_chunks else "(no relevant textbook context found)"
        prompt = f"""You are an exam tutor. Below is a transcribed exam question with its answer choices, and relevant excerpts retrieved from a reference textbook.

QUESTION:
{transcript}

RETRIEVED TEXTBOOK CONTEXT:
{context_text}

Your response must have exactly two parts:

1. A single line: "CORRECT_ANSWER: x" where x is exactly one letter (a, b, c, or d).
2. A blank line, then an HTML fragment (and nothing else after it) in exactly this structure:

<div class="ai-explanation">
  <h4>Explanation</h4>
  <p>...</p>
  <h5>Why the correct answer is correct</h5>
  <p>...</p>
  <h5>Why the other choices are incorrect</h5>
  <ul>
    <li>...</li>
  </ul>
  <h5>Key concept</h5>
  <p>...</p>
</div>

Rules:
- HTML only, no Markdown, no ```html code fences.
- Concise but educational.
- Base the explanation primarily on the retrieved textbook context above.
- If the context is insufficient to fully explain the answer, say so plainly rather than inventing information.
- No <script> tags, no JavaScript, no external resources (images/links), no attributes other than the class shown above."""

        raw = self._call_gemini(api_key, model, [{"text": prompt}])
        return self._parse_response(raw)

    def _parse_response(self, raw: str) -> tuple[str, str]:
        match = re.search(r"CORRECT_ANSWER:\s*([a-dA-D])", raw)
        if not match:
            raise ValueError(f"Could not parse CORRECT_ANSWER from model response: {raw[:200]}")
        answer_letter = match.group(1).lower()

        # Everything from the first '<' onward is the HTML fragment.
        html_start = raw.find("<")
        if html_start == -1:
            raise ValueError(f"No HTML fragment found in model response: {raw[:200]}")
        html = raw[html_start:].strip()
        # Strip accidental markdown code fences if the model added them anyway.
        html = re.sub(r"^```(?:html)?\s*|\s*```$", "", html.strip())
        return answer_letter, html

    def _append_log(self, rows: list):
        file_exists = os.path.isfile(LOG_PATH)
        with open(LOG_PATH, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["timestamp", "folder", "question", "status", "error"])
            ts = time.strftime("%Y-%m-%d %H:%M:%S")
            for folder, question_id, status, error in rows:
                writer.writerow([ts, folder, question_id, status, error])
