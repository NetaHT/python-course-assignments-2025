**Repository Guidance for Copilot**

This repository contains a single analysis script `Work life balance vs longevity.py` that loads a CSV dataset, computes distributions and correlations, and writes plot images to a `plots/` directory.

**Purpose**: help a developer (or Copilot) understand, run, and safely modify the script.

**How to run**
- **Install dependencies**: `pip install pandas numpy matplotlib seaborn`
- **Run the script** from the script directory (or give the full path):
  - `python "Work life balance vs longevity.py"`
- The script uses `DATA_PATH` (hard-coded at the top) to locate the CSV. Update that variable if the dataset is moved.

**What the script does**
- Loads the CSV at `DATA_PATH` into a `pandas.DataFrame`.
- Detects categorical columns (`gender`, `occupation_type`) and plots their distributions.
- Detects numeric columns and produces histogram plots (KDE) for each (excludes `id`).
- Creates scatter+regression plots comparing selected columns to `age_at_death`.
- Computes a Work-life-balance index: `(rest + sleep + exercise) / (rest + sleep + exercise + work)` and produces a separate scatter+regression plot of this index vs `age_at_death` for each occupation.
- Saves all plots into a `plots/` folder next to the script.

**Files generated**
- `plots/*.png` — one file per plot. Filenames are descriptive, for example:
  - `gender_distribution.png`
  - `avg_sleep_hours_per_day_hist.png`
  - `avg_sleep_hours_per_day_vs_age_at_death_corr.png`
  - `work_life_balance_index_vs_age_at_death_by_Teacher.png`

**Notes for Copilot / Recommendations for changes**
- When suggesting edits, prefer small, focused changes (fixes, readability, tests) over large refactors.
- Use the existing `find_column()` helper to detect columns by common keywords. If adding new keywords, keep them conservative and documented.
- Avoid changing the hard-coded `DATA_PATH` except when the user explicitly asks; instead expose it via a CLI argument if making the script more flexible.
- Keep plots saved to `plots/` and return filenames printed to stdout for reproducibility.

**Suggested incremental improvements**
- Add CLI options (via `argparse`) for `--data-path`, `--out-dir`, `--dpi`, and `--no-save`.
- Add a small `requirements.txt` or `pyproject.toml` for reproducible installs.
- Provide a Jupyter notebook that loads the generated plots and includes short interpretations.

**If asked to change plotting behaviour**
- Changing titles: replace underscores with spaces in display strings: `display = col.replace('_', ' ')`.
- Excluding columns: check name equality (case-insensitive) and prefer a small whitelist/blacklist approach.
- Faceting: use `seaborn.FacetGrid` or `plt.subplots()` with a deterministic order of occupations.

**Contact / context**
- The script was written to be runnable headless (it sets `MPLBACKEND=Agg` when run in CI or automated environments).
- If the user requests additional outputs (CSV with computed indices, PDF report, annotated plots), suggest adding flags and implementing them as small, testable functions.

**Example quick change request**
- "Add an argument `--min-occupation-samples` to only plot occupations with at least N samples." — implement with `argparse`, apply filter `df.groupby(occupation_col).filter(lambda g: len(g) >= N)`.

Thank you — follow these instructions when editing or suggesting edits to `Work life balance vs longevity.py`.
