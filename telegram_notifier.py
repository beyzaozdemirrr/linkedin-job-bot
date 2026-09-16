"""Telegram Bot API ile güvenli HTML iş ilanı bildirimi gönderimi."""

import html
from collections.abc import Mapping

import requests

from config import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN


def validate_telegram_config() -> None:
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        raise RuntimeError(
            "TELEGRAM_TOKEN ve TELEGRAM_CHAT_ID .env dosyasında tanımlanmalıdır."
        )


def _value(job: object, dictionary_key: str, attribute_name: str, default: str) -> str:
    """İlan verisini hem sözlükten hem de Job nesnesinden güvenli biçimde alır."""
    if isinstance(job, Mapping):
        return str(job.get(dictionary_key, default))
    return str(getattr(job, attribute_name, default))


def send_job(job: object, matched_keywords: list[str]) -> None:
    """İlanı Telegram'a HTML parser hatalarından korunmuş şekilde gönderir."""
    validate_telegram_config()
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    # HTML özel karakterlerini güvenli hâle getir.
    title = html.escape(_value(job, "title", "title", "İlan Title Yok"))
    company = html.escape(_value(job, "company", "company", "Şirket Belirtilmemiş"))
    location = html.escape(_value(job, "location", "location", "Konum Belirtilmemiş"))
    job_url = html.escape(_value(job, "link", "url", "#"), quote=True)
    keywords_str = html.escape(", ".join(matched_keywords))

    message = (
        f"🎯 <b>Yeni İlan Eşleşti!</b>\n\n"
        f"📌 <b>Başlık:</b> {title}\n"
        f"🏢 <b>Şirket:</b> {company}\n"
        f"📍 <b>Konum:</b> {location}\n"
        f"🔑 <b>Eşleşenler:</b> {keywords_str}\n\n"
        f"🔗 <a href='{job_url}'>İlana Git / Başvur</a>"
    )
    response = requests.post(
        url,
        json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
        },
        timeout=10,
    )

    # Telegram 400 vb. döndürürse API'nin ayrıntısı terminal günlüğünde görünür.
    if not response.ok:
        print(f"Telegram API Hata Detayı: {response.text}")
    response.raise_for_status()
