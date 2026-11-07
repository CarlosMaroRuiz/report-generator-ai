import html

from markdown import markdown

from worker.schemas import Report

CSS = """
@page { size: A4; margin: 22mm 18mm 24mm;
  @bottom-center { content: counter(page) " / " counter(pages); font-size: 8.5pt; color: #8a8a8a; } }
body { font: 11pt/1.6 "DejaVu Sans", sans-serif; color: #171717; }
h1 { font-size: 23pt; line-height: 1.15; margin: 0 0 6px; }
.subtitle { color: #555; font-style: italic; margin: 0 0 20px; }
.meta { font-size: 8.5pt; color: #777; border-top: 1px solid #dcdcdc;
        border-bottom: 1px solid #dcdcdc; padding: 7px 0; margin-bottom: 26px; }
.summary { background: #f5f6f8; border-left: 4px solid #333; padding: 14px 18px;
           break-inside: avoid; }
h2 { font-size: 14pt; margin: 26px 0 8px; padding-bottom: 4px;
     border-bottom: 2px solid #eaeaea; break-after: avoid; }
p { margin: 0 0 10px; text-align: justify; hyphens: auto; }
ul { margin: 6px 0 12px 20px; } li { margin: 3px 0; }
.note { margin-top: 28px; padding-top: 10px; border-top: 1px solid #eaeaea;
        font-size: 8.5pt; color: #888; }
"""

def _md(t: str) -> str:
    return markdown(t, extensions=['sane_lists', 'nl2br'])

def build_html(report: Report, meta: dict) -> str:
    e = html.escape
    sections = ''.join(
        f'<section><h2>{e(s.heading)}</h2>{_md(s.body)}'
        + (f'<ul>{"".join(f"<li>{e(b)}</li>" for b in s.bullets)}</ul>' if s.bullets else '')
        + '</section>'
        for s in report.sections
    )
    sources = (f'<section><h2>Fuentes y notas</h2><ul>'
               f'{"".join(f"<li>{e(x)}</li>" for x in report.sources)}</ul></section>'
               if report.sources else '')
    periodo = (f'<div>Periodo: {e(meta["start_date"])} → {e(meta["end_date"])}</div>'
               if meta.get('start_date') and meta.get('end_date') else '')
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>{e(report.title)}</title><style>{CSS}</style></head><body>
<h1>{e(report.title)}</h1><p class="subtitle">{e(report.subtitle)}</p>
<div class="meta"><div>Generado: {e(meta['generated_at'])}</div>{periodo}
<div>Modelo: {e(meta['model'])} · Job: {e(meta['task_id'])}</div></div>
<div class="summary"><h2>Resumen ejecutivo</h2>{_md(report.executive_summary)}</div>
{sections}
<section><h2>Conclusión</h2>{_md(report.conclusion)}</section>
{sources}
<p class="note">Documento generado automáticamente. Verifique cifras y citas antes de su uso formal.</p>
</body></html>"""