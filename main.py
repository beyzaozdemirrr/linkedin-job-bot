"""LinkedIn iş ilanı bildirim botu giriş noktası."""

import logging

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


def check_new_jobs() -> None:
    """Yeni, uygun ilanları bulur, iletir ve yalnızca başarılı iletimleri kaydeder."""
    try:
        jobs = fetch_jobs()
        logger.info("LinkedIn'den %d ilan alındı.", len(jobs))
    except Exception:
        logger.exception("LinkedIn ilanları alınamadı.")
        return

    sent_count = 0
    for job in jobs:
        try:
            if is_seen(job.job_id):
                continue

            is_match, matched_keywords = matches_cv(job.title, job.card_text)
            if not is_match:
                continue

            send_job(job, matched_keywords)
            mark_as_seen(job.job_id)
            sent_count += 1
            logger.info("İlan bildirildi: %s (%s)", job.title, job.job_id)
        except Exception:
            logger.exception("İlan işlenemedi: %s (%s)", job.title, job.job_id)

    logger.info("Tur tamamlandı: %d uygun yeni ilan bildirildi.", sent_count)


def main() -> None:
    initialize_database()
    validate_telegram_config()

    scheduler = BlockingScheduler(timezone="Europe/Istanbul")
    scheduler.add_job(
        check_new_jobs,
        trigger="interval",
        minutes=15,
        id="linkedin_job_checker",
        max_instances=1,
        coalesce=True,
    )
    logger.info("Bot başlatıldı; 15 dakikada bir kontrol yapılacak.")
    check_new_jobs()  # Başlangıçta ilk kontrolü hemen yap.
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot durduruldu.")


if __name__ == "__main__":
    main()
