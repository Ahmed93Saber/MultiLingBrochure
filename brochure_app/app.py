from __future__ import annotations
import gradio as gr
from .scraper import Website
from .prompting import SYSTEM_PROMPT, build_user_prompt
from .llm import stream_gpt

def stream_brochure(company_name: str, url: str, language: str):
    if not url or not url.startswith(("http://", "https://")):
        yield "Please enter a valid URL starting with http:// or https://"
        return

    yield "Fetching website..."
    site = Website(url).get_contents()

    yield "Building prompt..."
    prompt = build_user_prompt(company_name.strip() or "(Company)", language, site)

    yield "Generating brochure..."
    for partial in stream_gpt(prompt, system_prompt=SYSTEM_PROMPT):
        yield partial

def build_interface() -> gr.Interface:
    return gr.Interface(
        fn=stream_brochure,
        inputs=[
            gr.Textbox(label="Company name"),
            gr.Textbox(label="Landing page URL (include http:// or https://)"),
            gr.Dropdown(
                ["English", "Deutsch (German)", "Español (Spanish)", "Français (French)"],
                label="Language",
                value="English",
            ),
        ],
        outputs=[gr.Markdown(label="Brochure")],
        allow_flagging="never",
        title="Website → Brochure",
        description="Scrape a website and draft a one-page brochure in your chosen language.",
    )

def main():
    ui = build_interface()
    ui.launch()

if __name__ == "__main__":
    main()
