"""
generate_screening_pdf.py
─────────────────────────
Converte um relatório de screening Markdown (ClaudeTrader) em PDF profissional A4.

Uso:
    python scripts/generate_screening_pdf.py screenings/2026-03-17-screening.md
    python scripts/generate_screening_pdf.py screenings/2026-03-17-screening.md --output relatorios/custom.pdf

Dependências:
    pip install weasyprint markdown
"""

import argparse
import os
import re
import sys
from pathlib import Path

import markdown
from weasyprint import HTML


CSS_CONTENT = """
@page {
  size: A4;
  margin: 1.8cm 1.5cm 2cm 1.5cm;
  @bottom-center {
    content: "ClaudeTrader — Análise B3 | Página " counter(page) " de " counter(pages);
    font-size: 8pt;
    color: #888;
    font-family: "DejaVu Sans", Arial, sans-serif;
  }
}

* { box-sizing: border-box; }

body {
  font-family: "DejaVu Sans", "Liberation Sans", Arial, sans-serif;
  font-size: 10pt;
  line-height: 1.6;
  color: #1a1a2e;
  margin: 0;
  padding: 0;
}

h1 {
  font-size: 18pt;
  color: #0d47a1;
  border-bottom: 3px solid #0d47a1;
  padding-bottom: 6px;
  margin-top: 0;
  page-break-after: avoid;
}

h2 {
  font-size: 13pt;
  color: #1565c0;
  border-left: 4px solid #1565c0;
  padding-left: 10px;
  margin-top: 20px;
  margin-bottom: 8px;
  page-break-after: avoid;
  page-break-before: auto;
}

h3 {
  font-size: 11pt;
  color: #1976d2;
  margin-top: 16px;
  margin-bottom: 6px;
  page-break-after: avoid;
}

h2 + table, h3 + table, h2 + p + table {
  page-break-before: avoid;
}

p { margin: 6px 0 10px 0; }

table {
  width: 100%;
  border-collapse: collapse;
  margin: 10px 0 16px 0;
  font-size: 7pt;
  page-break-inside: avoid;
  table-layout: auto;
  word-break: break-word;
}

thead tr {
  background-color: #1565c0;
  color: white;
}

th {
  padding: 4px 5px;
  text-align: left;
  font-weight: bold;
  font-size: 6.8pt;
  white-space: nowrap;
}

td {
  padding: 3px 5px;
  border-bottom: 1px solid #e0e0e0;
  vertical-align: top;
  white-space: nowrap;
}

tr:nth-child(even) td { background-color: #f5f8ff; }

blockquote {
  background: #e3f2fd;
  border-left: 4px solid #1565c0;
  margin: 10px 0;
  padding: 8px 14px;
  border-radius: 0 4px 4px 0;
  page-break-inside: avoid;
  font-size: 9.5pt;
}

code {
  background: #f0f0f0;
  padding: 1px 4px;
  border-radius: 3px;
  font-size: 8.5pt;
  font-family: "DejaVu Sans Mono", "Courier New", monospace;
}

pre {
  background: #1e1e2e;
  color: #cdd6f4;
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 8pt;
  page-break-inside: avoid;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: "DejaVu Sans Mono", "Courier New", monospace;
  margin: 8px 0;
}

pre code {
  background: transparent;
  padding: 0;
  color: inherit;
  font-size: inherit;
}

hr {
  border: none;
  border-top: 1px solid #e0e0e0;
  margin: 16px 0;
}

ul, ol {
  margin: 6px 0 10px 0;
  padding-left: 20px;
}

li { margin: 3px 0; }

strong { color: #0d47a1; }

em { color: #546e7a; }

.disclaimer {
  font-size: 8pt;
  color: #9e9e9e;
  border-top: 1px solid #e0e0e0;
  padding-top: 8px;
  margin-top: 24px;
  page-break-inside: avoid;
}

.section-block {
  page-break-inside: avoid;
}
"""


def build_cover(title: str, date_str: str) -> str:
    return f"""
<div style="text-align:center; padding-top: 6cm; page-break-after: always;">
  <div style="font-size: 26pt; color: #0d47a1; font-weight: bold; margin-bottom: 12px;">
    {title}
  </div>
  <div style="font-size: 14pt; color: #546e7a; margin-bottom: 8px;">
    ClaudeTrader | Análise Fundamentalista + Técnica
  </div>
  <div style="font-size: 11pt; color: #78909c; margin-bottom: 40px;">
    Swing Trading · Dave Landry · RSI Wilder · EMA Trend
  </div>
  <div style="font-size: 10pt; color: #9e9e9e;">
    Gerado em {date_str}
  </div>
  <div style="margin-top: 60px; font-size: 8pt; color: #bdbdbd; font-style: italic;">
    Não constitui recomendação de investimento.
  </div>
</div>
"""


def wrap_h3_sections(html: str) -> str:
    """Wrap each h3 section in a section-block div to prevent mid-card page breaks."""
    parts = re.split(r'(?=<h3)', html)
    wrapped = []
    for part in parts:
        if part.startswith('<h3'):
            wrapped.append(f'<div class="section-block">{part}</div>')
        else:
            wrapped.append(part)
    return ''.join(wrapped)


def extract_title_and_date(md_text: str, source_path: Path) -> tuple[str, str]:
    """Extract title from first H1 and date from filename or H1."""
    title_match = re.search(r'^#\s+(.+)$', md_text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else source_path.stem

    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', source_path.stem)
    if date_match:
        y, m, d = date_match.group(1).split('-')
        date_str = f'{d}/{m}/{y}'
    else:
        date_str = ''

    return title, date_str


def generate_pdf(source: str, output: str) -> None:
    source_path = Path(source).resolve()
    output_path = Path(output).resolve()

    if not source_path.exists():
        print(f"Erro: arquivo não encontrado: {source_path}", file=sys.stderr)
        sys.exit(1)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    md_text = source_path.read_text(encoding='utf-8')
    title, date_str = extract_title_and_date(md_text, source_path)

    md_converter = markdown.Markdown(
        extensions=['tables', 'toc', 'fenced_code', 'attr_list'],
        extension_configs={'toc': {'title': 'Índice'}},
    )
    html_body = md_converter.convert(md_text)
    html_body = wrap_h3_sections(html_body)

    cover_html = build_cover(title, date_str)

    full_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>{CSS_CONTENT}</style>
</head>
<body>
{cover_html}
<div class="report-body">
{html_body}
</div>
<div class="disclaimer">
  <em>Screening gerado automaticamente via pipeline ClaudeTrader | fundamentus + yfinance | {date_str}</em><br>
  <em>Não constitui recomendação de investimento. Use como ponto de partida para sua própria análise.</em>
</div>
</body>
</html>"""

    print(f"Gerando PDF: {output_path}")
    HTML(string=full_html, base_url='/').write_pdf(str(output_path))

    size_kb = output_path.stat().st_size / 1024
    print(f"PDF salvo em: {output_path}  ({size_kb:.1f} KB)")


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Converte screening Markdown do ClaudeTrader em PDF profissional A4.'
    )
    parser.add_argument('source', help='Arquivo Markdown de entrada (ex: screenings/2026-03-17-screening.md)')
    parser.add_argument('--output', '-o', help='Caminho do PDF de saída (padrão: mesmo diretório do source)')
    args = parser.parse_args()

    source_path = Path(args.source)
    if args.output:
        output_path = args.output
    else:
        output_path = str(source_path.with_suffix('.pdf'))

    generate_pdf(args.source, output_path)


if __name__ == '__main__':
    main()
