"""İlanların CV ile uyumluluğunu kontrol eden filtreler."""

MUST_HAVE_KEYWORDS = [
    # Teknolojiler ve uzmanlık alanları
    "react", "node", "node.js", "express", "mongodb", "asp.net", "c#",
    ".net", "kotlin", "python", "sql", "docker", "mern", "frontend",
    "backend", "full stack", "fullstack", "javascript", "typescript", "api",
    "web", "mobile", "android", "ai",
    # Hedef iş unvanları
    "software engineer", "software developer", "yazılım uzmanı",
    "junior software engineer", "associate software engineer",
    "software development engineer", "application developer", "uygulama geliştirici",
    "full stack developer", "full stack engineer", "fullstack software developer",
    "web developer", "web geliştirici", "mern stack developer", "backend developer",
    "backend engineer", "node.js developer", ".net developer", "asp.net developer",
    "c# developer", "api developer", "frontend developer", "frontend engineer",
    "react developer", "javascript developer", "typescript developer",
    "mobile developer", "android developer", "kotlin developer", "ai software engineer",
    "developer",
]

EXCLUDE_KEYWORDS = [
    "senior", "lead", "manager", "director", "architect", "php",
    "wordpress", "ios", "swift", "flutter",
]


def matches_cv(title: str, description: str = "") -> tuple[bool, list[str]]:
    """Başlık ve açıklamaya göre CV uyumluluğunu ve eşleşmeleri döndürür."""
    searchable_text = f"{title or ''} {description or ''}".casefold()

    if any(keyword.casefold() in searchable_text for keyword in EXCLUDE_KEYWORDS):
        return False, []

    matched_keywords = [
        keyword for keyword in MUST_HAVE_KEYWORDS
        if keyword.casefold() in searchable_text
    ]
    return (True, matched_keywords) if matched_keywords else (False, [])
