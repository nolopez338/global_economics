from pathlib import Path
p=Path('tmp/solution-context-review/check-final-pdf.py')
s=p.read_text()+"\nfirst_page=r.pages[0].extract_text()\nfor title in ['Retail electricity costs','Savings-account interest','Summarized Solutions']:\n assert title in first_page, ('Contents entry missing',title)\nprint('Contents entries are present on page 1.')\n"
p.write_text(s)
