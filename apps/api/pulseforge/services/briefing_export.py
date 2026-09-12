from __future__ import annotations

from html import escape

from pulseforge.domain.models import Briefing


def briefing_to_html(briefing: Briefing) -> str:
    def items(values: list[str]) -> str:
        return "".join(f"<li>{escape(value)}</li>" for value in values)

    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{escape(briefing.title)}</title>
<style>
body{{font:15px/1.55 system-ui,sans-serif;max-width:900px;margin:48px auto;padding:0 24px;color:#15171a}}
h1,h2{{letter-spacing:-.02em}} .meta{{color:#667085}} code{{background:#f2f4f7;padding:2px 5px}}
</style></head><body>
<h1>{escape(briefing.title)}</h1>
<p class="meta">{briefing.period_start.isoformat()} → {briefing.period_end.isoformat()}</p>
<h2>Executive summary</h2><p>{escape(briefing.executive_summary)}</p>
<h2>Top developments</h2><ul>{items(briefing.top_developments)}</ul>
<h2>Emerging signals</h2><ul>{items(briefing.emerging_signals)}</ul>
<h2>Entity movements</h2><ul>{items(briefing.entity_movements)}</ul>
<h2>Contradictions / uncertainty</h2><ul>{items(briefing.contradictions)}</ul>
<h2>Watch list</h2><ul>{items(briefing.watch_list)}</ul>
<h2>Evidence</h2><p>{escape(", ".join(briefing.evidence_ids))}</p>
</body></html>"""


def briefing_to_pdf(briefing: Briefing) -> bytes:
    """Create a compact PDF without browser-side rendering."""
    from fpdf import FPDF

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.multi_cell(0, 10, briefing.title)
    pdf.set_font("Helvetica", size=9)
    pdf.multi_cell(0, 6, f"{briefing.period_start.isoformat()} -> {briefing.period_end.isoformat()}")

    sections = [
        ("Executive summary", [briefing.executive_summary]),
        ("Top developments", briefing.top_developments),
        ("Emerging signals", briefing.emerging_signals),
        ("Entity movements", briefing.entity_movements),
        ("Contradictions / uncertainty", briefing.contradictions),
        ("Watch list", briefing.watch_list),
        ("Evidence", briefing.evidence_ids),
    ]
    for heading, values in sections:
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 12)
        pdf.multi_cell(0, 7, heading)
        pdf.set_font("Helvetica", size=10)
        for value in values:
            pdf.multi_cell(0, 6, f"- {value}")
    return bytes(pdf.output())
