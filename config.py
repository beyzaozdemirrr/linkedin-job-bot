"""Uygulamanın tek noktadan yönetilen ayarları."""

import os
from dotenv import load_dotenv

load_dotenv()

LINKEDIN_SEARCH_URL = (
    "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
)
SEARCH_PARAMS = {
    "keywords": "Software Engineer",
    "location": "Turkey",
    "f_WT": "2,3",  # Remote ve Hybrid
    "f_TPR": "r86400",  # Son 24 saat
}

MUST_HAVE_KEYWORDS = [
    "react", "node", "express", "mongodb", "asp.net", "c#", ".net",
    "kotlin", "python", "sql", "docker", "mern", "frontend", "backend",
    "full stack", "software engineer", "developer",
]

EXCLUDE_KEYWORDS = [
    "senior", "lead", "manager", "director", "architect", "php",
    "wordpress", "ios", "swift", "flutter",
]

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
# CHAT_ID, Docker/.env yapılandırmasıyla uyumluluk için desteklenir.
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or os.getenv("CHAT_ID", "")
DATABASE_PATH = os.getenv("DATABASE_PATH", "seen_jobs.db")
REQUEST_TIMEOUT_SECONDS = 20

"""CV uyumluluğu kontrolü."""

from config import EXCLUDE_KEYWORDS, MUST_HAVE_KEYWORDS


def matches_cv(*texts: str) -> tuple[bool, list[str]]:
    """Metinlerde dışlama kelimesi yoksa eşleşen zorunlu teknolojileri döndürür."""
    searchable_text = " ".join(text for text in texts if text).casefold()

    if any(keyword.casefold() in searchable_text for keyword in EXCLUDE_KEYWORDS):
        return False, []

    matched_keywords = [
        keyword for keyword in MUST_HAVE_KEYWORDS
        if keyword.casefold() in searchable_text
    ]
    return bool(matched_keywords), matched_keywords
