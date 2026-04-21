# spatial-notebooks

10-week learning project: Python → Jupyter → data analysis → GIS.
Goal: build a reusable "data exploration → visualization → spatial analysis → deliverable" capability chain.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12+.

```bash
uv sync                               # install dependencies
uv run python -m ipykernel install \
    --user --name spatial-notebooks   # register Jupyter kernel (one-time)
uv run jupyter lab                    # launch notebook server
```

## Daily commands

```bash
uv run ruff check .                         # lint (ruff natively reads .ipynb)
uv run ruff format .                        # auto-format
uv run mypy src tests                       # type check (strict mode on from Week 2)
uv run nbqa mypy notebooks                  # type check notebooks via nbqa bridge
uv run pytest                               # run tests
uv run summarize data/samples/nagoya_wards.csv   # CLI entry point (Week 1/2 practice)
```

Notebooks in `notebooks/` are tracked; the `src/` package is where reusable logic lives.
Extract a function from a notebook the **second** time you copy-paste it.

## Layout

```
notebooks/   # 3–5 learning notebooks, numbered by phase
src/         # reusable functions (tested)
tests/       # pytest smoke tests for src/
data/
  samples/   # tiny committed sample data
  raw/       # gitignored — real/private data goes here
scripts/     # optional helper scripts
```

## Learning path (10 weeks)

| Phase | Weeks | Focus | Milestone |
| --- | --- | --- | --- |
| 1 | 1–2 | Python fundamentals + typing | CLI tool passes `mypy --strict` |
| 2 | 3 | Jupyter workflow | Reproducible notebook exported to HTML |
| 3 | 4–5 | pandas / numpy / matplotlib / plotly | End-to-end load→clean→aggregate→plot on real data |
| 4 | 6–8 | GIS: CRS, shapely, geopandas, folium | Spatial analysis notebook on 名古屋市 open data |
| 5 | 9–10 | Integration & deliverables | Final notebook + team review + demo |

### Phase toggles

- **Week 2**: uncomment `strict = true` in `[tool.mypy]` in `pyproject.toml`.
- **Phase 4**: install optional heavy deps only when needed (e.g. `rasterio`, `kepler.gl`).

## Sharing cadence

- **Weekly**: Friday async update in Notion/Slack (one chart + 3 bullet points on what was learned).
- **Week 5 & 10**: live 15-min demo to the team.
- **Weekly tip**: add one entry to `docs/tips.md` — 10 tips by end of program.

## Definition of Done

- Anyone can `uv sync` and re-run any notebook end-to-end in under 30 minutes.
- `uv run pytest` is green on every `src/` module.
- The Phase 4 real-world notebook has been reviewed by at least one teammate.
