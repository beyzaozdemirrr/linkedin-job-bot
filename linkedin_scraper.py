"""LinkedIn herkese açık iş arama uç noktasından ilan alma işlemleri."""

from dataclasses import dataclass
import re

import requests
from bs4 import BeautifulSoup

from config import LINKEDIN_SEARCH_URL, REQUEST_TIMEOUT_SECONDS, SEARCH_PARAMS

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
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
    match = re.search(r"currentJobId=(\d+)|/view/(\d+)", link.get("href", "") if link else "")
    return next((part for part in match.groups() if part), None) if match else None


def fetch_jobs() -> list[Job]:
    """Arama sonuçlarının ilk sayfasını getirir; ağ/HTTP hatalarında istisna yükseltir."""
    response = requests.get(
        LINKEDIN_SEARCH_URL,
        params={**SEARCH_PARAMS, "start": 0},
        headers=HEADERS,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
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
