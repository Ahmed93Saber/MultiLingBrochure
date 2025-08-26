from __future__ import annotations
from typing import Optional
from .scraper import Website

SYSTEM_PROMPT = (
    "You are a precise, helpful marketing writer. "
    "Analyze the provided company website content and write an accurate, "
    "persuasive one-page brochure in clean Markdown. "
    "Keep facts consistent with the source. Avoid making up details."
)

def build_user_prompt(
    company_name: str, language: str, site: Website, max_chars: Optional[int] = 8000
) -> str:
    # Prepare a compact excerpt to avoid overlong prompts
    page = str(site)
    if max_chars and len(page) > max_chars:
        half = max_chars // 2
        page = page[:half] + "\n...\n" + page[-half:]

    return f"""
Please write a brochure **in {language}** for the company **{company_name}** based on the website content below.

Constraints and format:
- Use clear Markdown headings and bullet points.
- Sections: Overview, What we offer, Key benefits, Social proof (if any), Call-to-action.
- Keep it factual and faithful to the provided text; do not invent specifics.
- Tone: professional, concise, friendly.

Website title: {site.title or "(none)"}
URL: {site.url}

Website content:
{page}
"""

