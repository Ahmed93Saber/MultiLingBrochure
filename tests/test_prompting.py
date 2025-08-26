from brochure_app.scraper import Website
from brochure_app.prompting import build_user_prompt

def test_build_user_prompt_includes_bits():
    site = Website(url="https://acme.io", title="ACME", text="ACME builds widgets.", links=[])
    prompt = build_user_prompt("ACME Corp", "Deutsch (German)", site)
    assert "ACME Corp" in prompt
    assert "Deutsch (German)" in prompt
    assert "Website title: ACME" in prompt
    assert "ACME builds widgets." in prompt
