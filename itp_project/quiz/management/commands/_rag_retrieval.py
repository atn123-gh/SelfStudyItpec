"""
Small, dependency-light retrieval helper for the insertsolutions offline
utility. Not part of the website - only used when generating explanations.

Deliberately simple: TF-IDF over fixed-size text chunks, no vector DB, no
neural embedding model. This is a one-time preparation script for a small
demo, not a production RAG service - see README's "Known quirks" section.
"""
import os
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

RESOURCES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "utils", "resources"
)
TEXTBOOK_PATH = os.path.join(RESOURCES_DIR, "textbook.txt")
INDEX_CACHE_PATH = os.path.join(RESOURCES_DIR, ".tfidf_index_cache.pkl")

CHUNK_SIZE = 900  # characters
CHUNK_OVERLAP = 150


def _chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Fixed-size chunking, splitting on line boundaries where possible so
    chunks don't cut mid-sentence."""
    lines = text.splitlines()
    chunks = []
    current: list[str] = []
    current_len = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue
        current.append(line)
        current_len += len(line) + 1
        if current_len >= chunk_size:
            chunks.append(" ".join(current))
            # keep the tail of this chunk as overlap for the next one
            overlap_lines: list[str] = []
            overlap_len = 0
            for l in reversed(current):
                overlap_lines.insert(0, l)
                overlap_len += len(l) + 1
                if overlap_len >= overlap:
                    break
            current = overlap_lines
            current_len = overlap_len

    if current:
        chunks.append(" ".join(current))

    return [c for c in chunks if len(c) > 40]  # drop tiny fragments (headers, page numbers)


class TextbookIndex:
    """Loads (or builds+caches) a TF-IDF index over the textbook, and
    answers top-k similarity queries against it."""

    def __init__(self):
        self.chunks: list[str] = []
        self.vectorizer: TfidfVectorizer | None = None
        self.matrix = None
        self._load_or_build()

    def _load_or_build(self):
        if os.path.exists(INDEX_CACHE_PATH) and os.path.getmtime(INDEX_CACHE_PATH) > os.path.getmtime(TEXTBOOK_PATH):
            with open(INDEX_CACHE_PATH, "rb") as f:
                cached = pickle.load(f)
            self.chunks = cached["chunks"]
            self.vectorizer = cached["vectorizer"]
            self.matrix = cached["matrix"]
            return

        with open(TEXTBOOK_PATH, "r", encoding="utf-8") as f:
            text = f.read()

        self.chunks = _chunk_text(text)
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=20000)
        self.matrix = self.vectorizer.fit_transform(self.chunks)

        with open(INDEX_CACHE_PATH, "wb") as f:
            pickle.dump(
                {"chunks": self.chunks, "vectorizer": self.vectorizer, "matrix": self.matrix}, f
            )

    def top_k(self, query: str, k: int = 3) -> list[str]:
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.matrix)[0]
        top_indices = scores.argsort()[::-1][:k]
        return [self.chunks[i] for i in top_indices if scores[i] > 0]
