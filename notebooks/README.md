# notebooks

Numbered by phase so the learning order is obvious.

| File | Phase | Topic |
| --- | --- | --- |
| `01_python_basics.ipynb` | 1 (Week 1–2) | Python fundamentals, typing, calling into `src/` |
| `02_jupyter_workflow.ipynb` | 2 (Week 3) | Notebook discipline: reproducibility, HTML export |
| `03_data_analysis.ipynb` | 3 (Week 4–5) | pandas / numpy / matplotlib / plotly on real data |
| `04_gis_fundamentals.ipynb` | 4 (Week 6–8) | CRS, geopandas, folium, spatial joins |
| `05_final_report.ipynb` | 5 (Week 9–10) | End-to-end deliverable for team + boss |

Create each notebook when you start its phase — don't stub them all up front.

## House rules

- **Restart & Run All** must succeed before commit. Non-linear notebooks are the #1 source of "works on my machine".
- Import from `src/spatial_notebooks/` rather than copy-pasting functions between notebooks.
- Any variable holding raw/sensitive data stays in `data/raw/` (gitignored) and gets a comment explaining where to fetch it.
- Export final deliverables to HTML so non-Python readers (老板) can open in a browser:
  `uv run jupyter nbconvert --to html notebooks/05_final_report.ipynb`.
