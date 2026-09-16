"""İlanların CV ile uyumluluğunu kontrol eden filtreler."""

MUST_HAVE_KEYWORDS = [
    "react", "node", "express", "mongodb", "asp.net", "c#", ".net",
    "kotlin", "python", "sql", "docker", "mern", "frontend", "backend",
    "full stack", "software engineer", "developer", "web developer",
]

EXCLUDE_KEYWORDS = [
    "senior", "lead", "manager", "director", "architect", "php",
    "wordpress", "ios", "swift", "flutter",
]


def matches_cv(title: str, description: str = "") -> tuple[bool, list[str]]:
    """Başlık ve açıklamaya göre CV uyumluluğunu ve eşleşmeleri döndürür."""
    searchable_text = f"{title or ''} {description or ''}".lower()

    if any(keyword in searchable_text for keyword in EXCLUDE_KEYWORDS):
        return False, []

    matched_keywords = [
        keyword for keyword in MUST_HAVE_KEYWORDS
        if keyword in searchable_text
    ]
    return (True, matched_keywords) if matched_keywords else (False, [])
