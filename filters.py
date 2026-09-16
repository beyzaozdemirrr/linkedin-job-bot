"""İlanların CV ile uyumluluğunu kontrol eden filtreler."""

MUST_HAVE_KEYWORDS = [
    "react", "node", "express", "mongodb", "asp.net", ".net", "c#",
    "docker", "sql", "kotlin", "javascript", "typescript", "full stack",
    "backend", "frontend", "software developer", "web developer", "mobile developer",
]

EXCLUDE_KEYWORDS = [
    "Senior", "Sr.", "Lead", "Principal", "Architect", "Staff", "Manager",
    "Head of", "Director", "5+ years", "7+ years", "10+ years",
]

ALLOWED_LEVELS = [
    "Junior", "Entry Level", "Associate", "Mid-Level", "Intermediate",
    "New Grad", "Graduate", "Intern", "Stajyer",
]


def matches_cv(title: str, description: str = "") -> tuple[bool, list[str]]:
    """Teknoloji/unvan ve hedef deneyim seviyesiyle CV uyumunu döndürür."""
    searchable_text = f"{title or ''} {description or ''}".casefold()

    if any(keyword.casefold() in searchable_text for keyword in EXCLUDE_KEYWORDS):
        return False, []

    matched_keywords = [
        keyword for keyword in MUST_HAVE_KEYWORDS
        if keyword.casefold() in searchable_text
    ]
    if not matched_keywords:
        return False, []

    if not any(level.casefold() in searchable_text for level in ALLOWED_LEVELS):
        return False, []

    return True, matched_keywords
