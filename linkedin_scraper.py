"""LinkedIn herkese açık iş arama uç noktasından ilan alma işlemleri."""

from dataclasses import dataclass
import logging
import random
import re
import time

import requests
from bs4 import BeautifulSoup

from config import LINKEDIN_SEARCH_URL, REQUEST_TIMEOUT_SECONDS, SEARCH_PARAMS

logger = logging.getLogger(__name__)

SEARCH_TITLES = [
    "Software Engineer", "Software Developer", "Yazılım Uzmanı",
    "Junior Software Engineer", "Associate Software Engineer", "Software Development Engineer",
    "Application Developer", "Uygulama Geliştirici",
    "Full Stack Developer", "Full Stack Engineer", "Fullstack Software Developer",
    "Web Developer", "Web Geliştirici", "MERN Stack Developer",
    "Backend Developer", "Backend Engineer", "Node.js Developer",
    ".NET Developer", "ASP.NET Developer", "C# Developer", "API Developer",
    "Frontend Developer", "Frontend Engineer", "React Developer",
    "JavaScript Developer", "TypeScript Developer",
    "Mobile Developer", "Android Developer", "Kotlin Developer",
    "AI Software Engineer",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
    "Referer": "https://www.linkedin.com/jobs/search/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


@dataclass(frozen=True)
class Job:
    job_id: str
    title: str
    company: str
    location: str
    url: str
    card_text: str


def _text(element, selector: str) -> str:
    found = element.select_one(selector)
    return found.get_text(" ", strip=True) if found else "Bilinmiyor"


def _job_id(card) -> str | None:
    urn = card.get("data-entity-urn", "")
    match = re.search(r"(\d+)$", urn)
    if match:
        return match.group(1)

    link = card.select_one("a.base-card__full-link")
    href = link.get("href", "") if link else ""
    match = re.search(r"currentJobId=(\d+)|/view/(\d+)", href)
    return next((part for part in match.groups() if part), None) if match else None


def _parse_jobs(page_html: str) -> list[Job]:
    """LinkedIn sonuç HTML'inden geçerli iş kartlarını ayrıştırır."""
    soup = BeautifulSoup(page_html, "html.parser")
    jobs: list[Job] = []
    for card in soup.select("li div.base-card"):
        job_id = _job_id(card)
        link = card.select_one("a.base-card__full-link")
        if not job_id or not link or not link.get("href"):
            continue
        jobs.append(
            Job(
                job_id=job_id,
                title=_text(card, "h3.base-search-card__title"),
                company=_text(card, "h4.base-search-card__subtitle"),
                location=_text(card, "span.job-search-card__location"),
                url=link["href"].split("?")[0],
                card_text=card.get_text(" ", strip=True),
            )
        )
    return jobs


def fetch_jobs() -> list[Job]:
    """Her hedef unvanı sırayla arar, sonuçları birleştirir ve tekrarları kaldırır."""
    jobs_by_id: dict[str, Job] = {}

    for index, search_title in enumerate(SEARCH_TITLES):
        if index > 0:
            time.sleep(random.uniform(2, 5))

        try:
            response = requests.get(
                LINKEDIN_SEARCH_URL,
                params={**SEARCH_PARAMS, "keywords": search_title, "start": 0},
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            status_code = error.response.status_code if error.response is not None else None
            if status_code == 429:
                logger.warning(
                    "LinkedIn rate limit (429) uygulandı: %s. 15 saniye bekleniyor.",
                    search_title,
                )
                time.sleep(15)
                continue
            logger.exception("LinkedIn HTTP hatası: %s", search_title)
        except requests.RequestException:
            logger.exception("LinkedIn araması başarısız: %s", search_title)
        else:
            for job in _parse_jobs(response.text):
                jobs_by_id.setdefault(job.job_id, job)

    return list(jobs_by_id.values())
