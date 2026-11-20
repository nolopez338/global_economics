from pathlib import Path
p=Path('book2026-2027/preamble/graphs/specific_highlights_view.tex');s=p.read_text();s=s.replace(r'\input{specific_highlights.tex}',r'\input{specific_highlights.tex}'+'\n'+r'\usepackage{needspace}')
s=s.replace('% Each entry starts on a fresh page; longtable retains its native page breaks','% Keep entry headings with opening rows; longtable retains its native page breaks')
s=s.replace(r'\newcommand{\PreviewLegend}[2]{%',r'\newcommand{\PreviewLegend}[2]{%'+'\n'+r'  \Needspace{12\baselineskip}%')
s=s.replace(r'\subsection{',r'\Needspace{18\baselineskip}'+'\n'+r'\subsection{')
p.write_bytes(s.replace('\n','\r\n').encode())
