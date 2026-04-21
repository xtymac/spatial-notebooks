# Learning Plan — Python × Jupyter × GIS

> Build a reusable capability chain:
> **data exploration → visualization → spatial analysis → deliverables (charts/tables/reports/scripts)**
> to support GIS engineering and prototype validation.

## Timeline

| Phase | Content | Weeks | Milestone | Status |
| --- | --- | --- | --- | --- |
| 1 | Python fundamentals | 1–2 | Typed CLI script + mypy strict | ✅ Done |
| 2 | Jupyter workflow | 3 | Reproducible notebook → HTML | ⬜ |
| 3 | Data analysis + viz | 4–5 | Load → clean → aggregate → plot | ⬜ |
| 4 | GIS fundamentals | 6–8 | Spatial analysis on 名古屋市 data | ⬜ |
| 5 | Integration | 9–10 | All deliverables + team review | ⬜ |

---

## Phase 1 — Python fundamentals (Week 1–2) ✅

### What to learn

- **Package management**: `uv` (venv + deps + Python version in one tool)
- **Type hints**: `int`, `str`, `list[str]`, `dict[str, int]`, `X | None`
- **mypy**: default in Week 1, `strict = true` in Week 2
- **Data structures**: `list`, `dict`, `set`, `dataclass`, `Path`
- **I/O**: `Path.read_text()`, `pd.read_csv()`, `json.dumps()`

### Practice deliverable

CLI tool: `uv run summarize data/samples/nagoya_wards.csv`
- Reads CSV, prints summary stats as JSON
- Code: `src/spatial_notebooks/cli.py` → calls `src/spatial_notebooks/stats.py`
- Tests: `tests/test_stats.py` (7 tests)

### Week 1 checklist

- [x] Set up project: `uv sync`, register Jupyter kernel
- [x] Write `load_csv()` and `summarize()` in `stats.py`
- [x] Write `main()` CLI in `cli.py`
- [x] 5 pytest tests passing
- [x] `ruff check .` clean
- [x] Run notebook `01_python_basics.ipynb` end-to-end
- [x] Complete 3 exercises: density calc, boolean indexing, extract to src/
- [x] `add_density()` extracted with 2 additional tests
- [x] First tip in `docs/tips.md` (#01: don't use notebook cells to write .py files)

### Week 2 checklist

- [x] Flip `strict = true` in pyproject.toml `[tool.mypy]`
- [x] Add `py.typed` marker + `force-include` in build config
- [x] Add `nbqa` for notebook type checking
- [x] Add ruff per-file-ignore `B018` for notebooks
- [x] All code passes `mypy --strict`
- [x] Second tip (#02: py.typed is required for typed packages)
- [ ] Friday async update to Slack/Notion (Week 2)

### Key concepts learned

```python
# dataclass — typed container for structured results
@dataclass(frozen=True)
class Summary:
    rows: int
    columns: int

# Path — never use raw strings for file paths
from pathlib import Path
path = Path("data/samples/foo.csv")

# boolean indexing — pandas core operation
big_wards = df[df["area_km2"] > df["area_km2"].median()]

# .assign() — returns a new DataFrame, no side effects
df.assign(density=df["population"] / df["area_km2"])

# autoreload — live-reload src/ changes into notebook
%load_ext autoreload
%autoreload 2
```

---

## Phase 2 — Jupyter workflow (Week 3)

### What to learn

- **Notebook structure**: one clear narrative per notebook (question → data → analysis → conclusion)
- **Reproducibility**: `Restart & Run All` must succeed; pin deps with `uv.lock`
- **Exporting**: `jupyter nbconvert --to html` for non-technical readers (老板)
- **nbqa**: run mypy/ruff on notebook cells via `uv run nbqa mypy notebooks/`

### Practice deliverable

- `notebooks/02_jupyter_workflow.ipynb`: convert the Phase 1 CLI logic into an interactive notebook
- Export to HTML, send to a teammate — they must be able to run it from scratch with just `uv sync`

### Week 3 checklist

- [ ] Create `02_jupyter_workflow.ipynb`
- [ ] Notebook has clear Markdown sections: Goal → Data → Analysis → Conclusion
- [ ] Uses `%autoreload 2` to import from `src/`
- [ ] `Restart & Run All` succeeds
- [ ] Export to HTML: `uv run jupyter nbconvert --to html notebooks/02_jupyter_workflow.ipynb`
- [ ] Send HTML to one teammate — confirm they can read it
- [ ] Give teammate the repo — confirm `uv sync` + re-run works on their machine
- [ ] Tip #03 in `docs/tips.md`
- [ ] Friday async update

### Tips for this phase

- **Cell ordering rule**: never run cells out of order during development. If you need to experiment, add new cells at the bottom; merge back into narrative order before committing.
- **Markdown discipline**: every code cell should have a Markdown cell above it explaining *what question this cell answers*.
- **Output rule**: clear all outputs before commit (`Cell → Clear All Outputs`), unless the output is the whole point (charts, final results).

---

## Phase 3 — Data analysis + visualization (Week 4–5)

### What to learn

- **pandas**: `read_csv`, `groupby`, `merge`, `pivot_table`, `resample` (time series)
- **numpy**: vectorized ops, broadcasting, `np.where`
- **matplotlib**: figures, axes, subplots, `savefig`
- **plotly**: interactive charts, `px.bar`, `px.scatter_mapbox`

### Practice deliverable

- `notebooks/03_data_analysis.ipynb`: end-to-end pipeline on real data
- **Tie to real work**: use data from current projects — 名古屋市 open data, RFI analysis data, or any client-related dataset
- 5 charts that each answer a specific question (not just "here's a plot")
- Extract any reusable data-loading/cleaning functions to `src/spatial_notebooks/`

### Week 4 checklist

- [ ] Download a real dataset (名古屋市 open data portal or project data)
- [ ] Place raw data in `data/raw/` (gitignored), write loading script in `src/`
- [ ] Create `03_data_analysis.ipynb`
- [ ] Data cleaning pipeline: handle NaN, fix dtypes, normalize column names
- [ ] 3 exploratory plots with matplotlib (distribution, trend, comparison)
- [ ] Extract `clean_*()` functions to `src/` with tests
- [ ] Tip #04
- [ ] Friday async update

### Week 5 checklist

- [ ] 2 interactive plots with plotly
- [ ] At least one chart that tells a clear business story (not just EDA)
- [ ] Summary table output (styled with `df.style` or exported to CSV)
- [ ] Notebook narrative: question → method → finding → so what?
- [ ] Tip #05
- [ ] Week 5 live demo (15 min) to team 🎤
- [ ] Friday async update

### Useful pandas patterns

```python
# groupby + agg — the bread and butter
df.groupby("ward").agg(
    total_pop=("population", "sum"),
    avg_area=("area_km2", "mean"),
)

# method chaining — readable pipelines
result = (
    df
    .query("population > 100_000")
    .assign(density=lambda x: x["population"] / x["area_km2"])
    .sort_values("density", ascending=False)
    .head(10)
)

# pivot_table — for cross-tabulations
pd.pivot_table(df, values="population", index="region", columns="year", aggfunc="sum")
```

### Useful matplotlib patterns

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].bar(...)
axes[1].scatter(...)
axes[2].plot(...)
fig.suptitle("Overall title")
plt.tight_layout()
plt.savefig("output.png", dpi=150, bbox_inches="tight")
```

---

## Phase 4 — GIS fundamentals (Week 6–8)

### What to learn

- **CRS / EPSG**: WGS84 (`EPSG:4326`), Web Mercator (`EPSG:3857`), Japan Plane Rectangular (`JGD2011` / `EPSG:6675` for Zone 7 名古屋)
- **Projection transforms**: `gdf.to_crs(epsg=...)` — always transform to projected CRS before measuring distances/areas
- **Spatial predicates**: `within`, `intersects`, `contains`
- **Spatial operations**: `buffer`, `overlay`, `dissolve`, `sjoin` (spatial join)
- **File formats**: Shapefile, GeoJSON, GeoPackage (`.gpkg` — prefer this)
- **Tools**: shapely (geometry), geopandas (tabular + geometry), pyproj (CRS), folium (web maps)

### Practice deliverable

- `notebooks/04_gis_fundamentals.ipynb`: end-to-end spatial analysis on 名古屋市 GIS data
- Example analyses:
  - Ward boundary visualization on folium interactive map
  - Spatial join: POI count per ward
  - Buffer analysis: what's within 500m of each train station?
  - Area/perimeter calculation in projected CRS (not geographic!)

### Week 6 checklist

- [ ] Download 名古屋市 GIS data (ward boundaries as Shapefile/GeoJSON)
- [ ] Load with geopandas: `gpd.read_file("path.geojson")`
- [ ] Understand CRS: `gdf.crs`, `gdf.to_crs(epsg=6675)`
- [ ] Plot ward boundaries: `gdf.plot(column="ward", legend=True)`
- [ ] Create `notebooks/04_gis_fundamentals.ipynb`
- [ ] Tip #06
- [ ] Friday async update

### Week 7 checklist

- [ ] Spatial join: `gpd.sjoin(points_gdf, wards_gdf, predicate="within")`
- [ ] Buffer analysis: `gdf.buffer(500)` (in projected CRS)
- [ ] Area calculation: `gdf.to_crs(epsg=6675).area` (m²)
- [ ] Interactive folium map with popups
- [ ] Extract spatial utility functions to `src/spatial_notebooks/geo.py`
- [ ] Tip #07
- [ ] Friday async update

### Week 8 checklist

- [ ] Complete notebook narrative with clear conclusions
- [ ] At least one finding relevant to Eukarya/Re:Earth work
- [ ] All spatial functions tested in `tests/test_geo.py`
- [ ] Stretch goal: deck.gl / kepler.gl visualization (skip if time-tight)
- [ ] Tip #08
- [ ] Friday async update

### CRS pitfalls (very common)

```python
import geopandas as gpd

gdf = gpd.read_file("wards.geojson")
print(gdf.crs)  # usually EPSG:4326 (lat/lon degrees)

# ❌ WRONG — area in degrees² (meaningless)
gdf["area_bad"] = gdf.area

# ✅ CORRECT — project to meters first
gdf_proj = gdf.to_crs(epsg=6675)  # JGD2011 Zone 7 (Nagoya)
gdf_proj["area_m2"] = gdf_proj.area
gdf_proj["area_km2"] = gdf_proj.area / 1_000_000
```

### Useful GIS data sources

| Source | URL | Notes |
| --- | --- | --- |
| 名古屋市 open data | https://www.city.nagoya.jp/shisei/category/388-0-0-0-0-0-0-0-0-0.html | Ward boundaries, facilities |
| 国土数値情報 | https://nlftp.mlit.go.jp/ksj/ | National-level GIS data (roads, rivers, admin boundaries) |
| OpenStreetMap | https://download.geofabrik.de/asia/japan.html | POIs, roads, buildings |
| e-Stat | https://www.e-stat.go.jp/ | Census + boundaries (小地域) |

---

## Phase 5 — Integration & deliverables (Week 9–10)

### Final deliverables checklist

- [ ] **notebooks/**: 4–5 notebooks (01–05), all pass `Restart & Run All`
- [ ] **src/**: reusable modules with full type annotations and `py.typed`
- [ ] **tests/**: all green under `uv run pytest`
- [ ] **data/samples/**: committed sample data with README
- [ ] **docs/tips.md**: 10 entries complete
- [ ] **Final notebook** (`05_final_report.ipynb`): end-to-end analysis answering a concrete business question
- [ ] **HTML export** of final notebook for non-technical stakeholders
- [ ] **One real-world deliverable**: script/notebook that answers a concrete business question (e.g. coverage analysis, data quality audit for a client dataset)

### Week 9 checklist

- [ ] Create `notebooks/05_final_report.ipynb`
- [ ] Choose a real business question (coordinate with team/manager)
- [ ] Full pipeline: load → clean → analyze → visualize → conclude
- [ ] Tip #09
- [ ] Friday async update

### Week 10 checklist

- [ ] Polish all notebooks: clear narrative, clean code, no stale cells
- [ ] Complete `docs/tips.md` (tip #10)
- [ ] Run full CI check: `uv run ruff check . && uv run mypy src tests && uv run pytest`
- [ ] Export final report to HTML
- [ ] Get code review from at least one teammate
- [ ] Week 10 live demo (15 min) 🎤
- [ ] Final Friday async update — summary of the full 10-week journey

---

## Sharing cadence

### Weekly async update (every Friday, 15 min effort)

Post to Slack or Notion. Template:

```
📊 Week N 学习进度 · [Phase topic]

**本周学到**
• [一个技术点]
• [一个工程习惯]
• [一个坑]

**本周产出**
• [notebook / function / test]

**一张图**
[截图或导出的图表]

**下周计划**
• [Phase / milestone target]
```

### Live demos

- **Week 5**: data analysis pipeline demo (Phase 3 deliverable)
- **Week 10**: full-stack demo (final report + spatial analysis)
- Format: 15 minutes, screen share, walk through one notebook end-to-end
- Prep: `Restart & Run All` **before** the demo, not during

---

## Engineering standards

| Tool | Command | When |
| --- | --- | --- |
| ruff lint | `uv run ruff check .` | Before every commit |
| ruff format | `uv run ruff format .` | Before every commit |
| mypy | `uv run mypy src tests` | Before every commit |
| nbqa mypy | `uv run nbqa mypy notebooks/` | After editing notebooks |
| pytest | `uv run pytest` | Before every commit |
| Full check | `uv run ruff check . && uv run mypy src tests && uv run pytest` | Weekly + before demos |

### Code organization rule

> **Notebook** = narrative + exploration + visualization.
> **src/** = reusable functions + business logic.
> **tests/** = pytest tests for everything in src/.
>
> If you copy-paste a function a second time, move it to src/.

---

## Risks & mitigations

| Risk | Mitigation |
| --- | --- |
| Non-reproducible notebooks | `Restart & Run All` before every commit; `uv.lock` pins exact versions |
| Phase takes longer than timebox | Finish core exercise, move on; depth comes in later iterations |
| Spreading too wide on libraries | Prioritize libs that directly help current tasks (geopandas > rasterio > kepler.gl) |
| deck.gl / kepler.gl stretch goal | Skip if Phase 4 is tight; it's a "nice to have" |
| CRS bugs | Always check `gdf.crs` before spatial operations; always project before measuring |
| No real data available | Start with 名古屋市 open data; switch to project data when available |

## Definition of Done

- [ ] Anyone can `uv sync` and re-run any notebook end-to-end in ≤ 30 minutes
- [ ] `uv run pytest` is green on every `src/` module
- [ ] The Phase 4 real-world notebook has been reviewed by at least one teammate
- [ ] `docs/tips.md` has 10 entries
- [ ] Two live demos completed (Week 5 + Week 10)
