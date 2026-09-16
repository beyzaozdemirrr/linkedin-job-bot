"""Uygulamanın tek noktadan yönetilen ayarları."""

import os
from dotenv import load_dotenv

load_dotenv()

LINKEDIN_SEARCH_URL = (
    "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
)
SEARCH_PARAMS = {
    "location": "Turkey",
    "f_WT": "2,3",  # Remote ve Hybrid
    "f_TPR": "r86400",  # Son 24 saat
}

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
# CHAT_ID, Docker/.env yapılandırmasıyla uyumluluk için desteklenir.
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or os.getenv("CHAT_ID", "")
DATABASE_PATH = os.getenv("DATABASE_PATH", "seen_jobs.db")
REQUEST_TIMEOUT_SECONDS = 20
