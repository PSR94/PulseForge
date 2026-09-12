from pulseforge.services.briefing_export import briefing_to_html, briefing_to_pdf
from pulseforge.services.demo_repository import get_demo_repository


def test_briefing_exports_html_and_pdf():
    briefing = get_demo_repository().build_briefing()
    html = briefing_to_html(briefing)
    pdf = briefing_to_pdf(briefing)
    assert "<h1>24-Hour AI Industry Brief</h1>" in html
    assert pdf.startswith(b"%PDF")
