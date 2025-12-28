def clean_text(text: str) -> str:
    if not text:
        return ""
    cleaned = text.replace("\n", " ").replace("\t", " ")
    return " ".join(cleaned.split())