"""LinkedIn iş ilanı bildirim botu giriş noktası."""

import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

from apscheduler.schedulers.blocking import BlockingScheduler

from database import initialize_database, is_seen, mark_as_seen
from filters import matches_cv
from linkedin_scraper import fetch_jobs
from telegram_notifier import send_job, validate_telegram_config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


class HealthCheckHandler(BaseHTTPRequestHandler):
    """Render'ın servis erişilebilirlik denetimleri için basit HTTP yanıtı."""

    def do_GET(self) -> None:  # noqa: N802 - HTTP metodunun standart adı
        response_body = b"Bot is alive"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def log_message(self, format: str, *args: object) -> None:
        """Her health check isteğinin standart hata çıktısını doldurmasını önler."""


def start_health_check_server() -> threading.Thread:
    """HTTP health check sunucusunu ana scheduler'ı engellemeden başlatır."""
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    thread = threading.Thread(
        target=server.serve_forever,
        name="health-check-server",
        daemon=True,
    )
    thread.start()
    logger.info("Health check sunucusu %d portunda başlatıldı.", port)
    return thread


def fetch_and_process_jobs() -> None:
    """İlanları alır, filtreler, yeni eşleşmeleri iletir ve kaydeder."""
    try:
        jobs = fetch_jobs()
        logger.info("LinkedIn'den %d ilan alındı.", len(jobs))
    except Exception:
        logger.exception("LinkedIn ilanları alınamadı.")
        return

    filtered_count = 0
    sent_count = 0
    for job in jobs:
        try:
            is_match, matched_keywords = matches_cv(job.title, job.card_text)
            if not is_match:
                continue
            filtered_count += 1

            if is_seen(job.job_id):
                continue

            send_job(job, matched_keywords)
            mark_as_seen(job.job_id)
            sent_count += 1
            logger.info("İlan bildirildi: %s (%s)", job.title, job.job_id)
        except Exception:
            logger.exception("İlan işlenemedi: %s (%s)", job.title, job.job_id)

    logger.info(
        "Tur tamamlandı: toplam %d ilan, filtreyi geçen %d ilan, Telegram'a gönderilen %d ilan.",
        len(jobs),
        filtered_count,
        sent_count,
    )


def main() -> None:
    initialize_database()
    validate_telegram_config()
    start_health_check_server()

    scheduler = BlockingScheduler(timezone="Europe/Istanbul")
    scheduler.add_job(
        fetch_and_process_jobs,
        trigger="interval",
        minutes=15,
        id="linkedin_job_checker",
        max_instances=1,
        coalesce=True,
    )
    logger.info("Bot başlatıldı; 15 dakikada bir kontrol yapılacak.")
    fetch_and_process_jobs()  # Scheduler başlamadan ilk kontrolü hemen yap.
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot durduruldu.")


if __name__ == "__main__":
    main()
