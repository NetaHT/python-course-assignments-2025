# Work life balance vs. longevity

**Repository Guidance**

This repository contains a single analysis script `Work life balance vs longevity.py` that loads a CSV dataset, computes distributions and correlations, and writes plot images to a `plots/` directory.

**How to run**
- **Install dependencies**: `pip install pandas numpy matplotlib seaborn`
- **Run the script** from the script directory (or give the full path):
  - `python "Work life balance vs longevity.py"`
- The script uses `DATA_PATH` (hard-coded at the top) to locate the CSV. Download the CSV from github folder and change DATA_PATH accordingly.

**What the script does**
- Loads the CSV at `DATA_PATH` into a `pandas.DataFrame`.
- Detects categorical columns (`gender`, `occupation_type`) and plots their distributions.
- Detects numeric columns and produces histogram plots (KDE) for each (excludes `id`).
- Creates scatter+regression plots comparing selected columns to `age_at_death`.
- Computes a Work-life-balance index: `(rest + sleep + exercise) / (rest + sleep + exercise + work)` and produces a separate scatter+regression plot of this index vs `age_at_death` for each occupation.
- Saves all plots into a `plots/` folder next to the script- **saved to github as a seperate folder in day08 as an example**

**Files generated**
- `plots/*.png` — one file per plot. Filenames are descriptive, for example:
  - `gender_distribution.png`
  - `avg_sleep_hours_per_day_hist.png`
  - `avg_sleep_hours_per_day_vs_age_at_death_corr.png`
  - `work_life_balance_index_vs_age_at_death_by_Teacher.png`

**CLI options** (via `argparse`) `--data-path`, `--out-dir`, `--dpi`, and `--no-save`.
