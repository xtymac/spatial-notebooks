# data/samples

Small, **non-sensitive** sample datasets committed to the repo so notebooks are
runnable out-of-the-box.

| File | Description | Source |
| --- | --- | --- |
| `nagoya_wards.csv` | 16 wards of Nagoya: population, area, centroid lat/lon | Hand-compiled for learning; not authoritative — do not use for production analysis |

## Rules

- **Never** commit real customer data, RFI data, or anything flagged private.
- Keep sample files under ~100 KB; larger data goes in `data/raw/` (gitignored).
- Add a row to the table above whenever you commit a new sample file.
