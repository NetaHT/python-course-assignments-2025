"""
Load the provided dataset and generate distribution plots:
- distribution by gender (or sex column)
- distribution by occupation (or job/occupation type column)
- distributions for all other numeric columns (histogram + boxplot)

The script saves plots to a `plots/` directory next to this file.
"""
import os
import re
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

DATA_PATH = '/Users/netah/Library/CloudStorage/OneDrive-weizmann.ac.il/PhD- personal/courses/python/work life balance-longevity dataset.csv'
# default plots dir next to script; can be overridden by CLI
DEFAULT_PLOTS_DIR = os.path.join(os.path.dirname(__file__), 'plots')


def safe_fname(s: str) -> str:
	return re.sub(r"[^0-9a-zA-Z-_]+", '_', s).strip('_')


def find_column(df: pd.DataFrame, keywords):
	"""Return first column name that matches any keyword (case-insensitive), else None."""
	cols = df.columns
	for kw in keywords:
		for c in cols:
			if kw.lower() in str(c).lower():
				return c
	return None


def plot_categorical(df, col, plots_dir, dpi=100, no_save=False):
	if col is None:
		return None
	plt.figure(figsize=(8, 5))
	order = df[col].value_counts(dropna=False).index
	sns.countplot(data=df, x=col, order=order)
	plt.xticks(rotation=45, ha='right')
	display = str(col).replace('_', ' ')
	plt.title(f'Distribution of {display}')
	plt.tight_layout()
	out = os.path.join(plots_dir, f'{safe_fname(col)}_distribution.png')
	if no_save:
		print('(no-save) would write', out)
	else:
		plt.savefig(out, dpi=dpi)
	plt.close()
	return out


def plot_numeric(df, col, plots_dir, dpi=100, no_save=False):
	if col is None:
		return None
	# histogram + kde (no boxplot)
	plt.figure(figsize=(8, 5))
	sns.histplot(df[col].dropna(), kde=True)
	display = str(col).replace('_', ' ')
	plt.title(f'Histogram of {display}')
	plt.xlabel(display)
	plt.tight_layout()
	out = os.path.join(plots_dir, f'{safe_fname(col)}_hist.png')
	if no_save:
		print('(no-save) would write', out)
	else:
		plt.savefig(out, dpi=dpi)
	plt.close()
	return out


def plot_correlation(df, col, target_col, plots_dir, dpi=100, no_save=False):
	"""Scatter plot with regression line comparing `col` to `target_col` and report Pearson r."""
	if col is None or target_col is None:
		return None
	x = df[col]
	y = df[target_col]
	# Drop NA pairs
	pair = df[[col, target_col]].dropna()
	if pair.shape[0] < 3:
		return None
	x = pair[col]
	y = pair[target_col]
	# compute Pearson correlation
	try:
		r = np.corrcoef(x, y)[0, 1]
	except Exception:
		r = float('nan')

	plt.figure(figsize=(6, 5))
	sns.regplot(x=x, y=y, scatter_kws={'s': 15, 'alpha': 0.6}, line_kws={'color': 'red'})
	display_x = str(col).replace('_', ' ')
	display_y = str(target_col).replace('_', ' ')
	plt.title(f'{display_x} vs {display_y} (r={r:.2f})')
	plt.xlabel(display_x)
	plt.ylabel(display_y)
	plt.tight_layout()
	out = os.path.join(plots_dir, f'{safe_fname(col)}_vs_{safe_fname(target_col)}_corr.png')
	if no_save:
		print('(no-save) would write', out)
	else:
		plt.savefig(out, dpi=dpi)
	plt.close()
	return out


def main():
	parser = argparse.ArgumentParser(description='Plot distributions and correlations from work-life dataset')
	parser.add_argument('--data-path', default=DATA_PATH, help='Path to the CSV dataset')
	parser.add_argument('--out-dir', default=None, help='Directory to save plots (defaults to script/plots)')
	parser.add_argument('--dpi', type=int, default=100, help='DPI for saved plots')
	parser.add_argument('--no-save', action='store_true', help="Don't write plot files; just print what would be written")
	args = parser.parse_args()

	data_path = args.data_path
	plots_dir = args.out_dir or DEFAULT_PLOTS_DIR
	dpi = args.dpi
	no_save = args.no_save

	if not no_save:
		os.makedirs(plots_dir, exist_ok=True)

	# Try to read the CSV
	try:
		df = pd.read_csv(data_path)
	except Exception as e:
		print(f'Error reading CSV at {data_path}: {e}')
		return

	print('Loaded dataset with shape:', df.shape)
	print('Columns:', list(df.columns))

	# Basic cleaning of column names
	df.columns = [str(c).strip() for c in df.columns]

	# Find gender and occupation columns with common keywords
	gender_col = find_column(df, ['gender', 'sex'])
	occupation_col = find_column(df, ['occupation', 'job', 'occupation type', 'work type'])

	created = []

	if gender_col:
		print('Found gender column:', gender_col)
		created.append(plot_categorical(df, gender_col, plots_dir, dpi=dpi, no_save=no_save))
	else:
		print('No gender/sex column detected automatically.')

	if occupation_col:
		print('Found occupation column:', occupation_col)
		created.append(plot_categorical(df, occupation_col, plots_dir, dpi=dpi, no_save=no_save))
	else:
		print('No occupation/job column detected automatically.')

	# Numeric columns: plot distribution for each (exclude id)
	numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c]) and str(c).lower() != 'id']
	if numeric_cols:
		print('Numeric columns detected:', numeric_cols)
		for c in numeric_cols:
			created.append(plot_numeric(df, c, plots_dir, dpi=dpi, no_save=no_save))
	else:
		# Try to coerce columns to numeric and retry
		coerced = []
		for c in df.columns:
			coerced_col = pd.to_numeric(df[c], errors='coerce')
			if coerced_col.notna().sum() > 0 and coerced_col.nunique() > 1:
				df[c + '_coerced_num'] = coerced_col
				coerced.append(c + '_coerced_num')
		if coerced:
			print('Coerced numeric-like columns:', coerced)
			for c in coerced:
				created.append(plot_numeric(df, c, plots_dir, dpi=dpi, no_save=no_save))
		else:
			print('No numeric columns found to plot.')

	# For non-numeric columns other than gender/occupation, plot top categories
	other_object_cols = [c for c in df.select_dtypes(include=['object', 'category']).columns if c not in (gender_col, occupation_col)]
	for c in other_object_cols:
		# only plot if not too many unique values
		if df[c].nunique(dropna=False) <= 30:
			plt.figure(figsize=(8, 5))
			order = df[c].value_counts(dropna=False).index
			sns.countplot(data=df, x=c, order=order)
			plt.xticks(rotation=45, ha='right')
			display = str(c).replace('_', ' ')
			plt.title(f'Distribution of {display}')
			plt.tight_layout()
			out = os.path.join(plots_dir, f'{safe_fname(c)}_distribution.png')
			if no_save:
				print('(no-save) would write', out)
			else:
				plt.savefig(out, dpi=dpi)
			plt.close()
			created.append(out)

	# Create correlation plots for columns 4-7 (1-based) vs age_at_death
	# Use positional selection to satisfy the user's request: columns 4-7 correspond to indices 3..6
	target_col = find_column(df, ['age_at_death', 'age at death', 'age'])
	if target_col is None:
		print('Could not detect age/age_at_death column for correlation plots.')
	else:
		cols_for_corr = []
		try:
			all_cols = list(df.columns)
			# ensure indices exist
			if len(all_cols) >= 7:
				cols_for_corr = all_cols[3:7]
			else:
				# fallback: use all numeric columns except id and target
				cols_for_corr = [c for c in numeric_cols if c != target_col]
		except Exception:
			cols_for_corr = [c for c in numeric_cols if c != target_col]

		corr_created = []
		for c in cols_for_corr:
			# ensure column is numeric or coercible
			if not pd.api.types.is_numeric_dtype(df[c]):
				coerced = pd.to_numeric(df[c], errors='coerce')
				if coerced.notna().sum() < 3:
					continue
				df['_tmp_coerced'] = coerced
				src_col = '_tmp_coerced'
			else:
				src_col = c
			out = plot_correlation(df, src_col, target_col, plots_dir, dpi=dpi, no_save=no_save)
			if out:
				corr_created.append(out)
		if corr_created:
			print('Created correlation plots:')
			for p in corr_created:
				print('-', p)

		# --- Work-life balance index: compute and plot per occupation type ---
		# Identify columns for work/rest/sleep/exercise
		work_col = find_column(df, ['work', 'work_hours', 'work_hours_per_day', 'avg_work'])
		rest_col = find_column(df, ['rest', 'rest_hours', 'avg_rest'])
		sleep_col = find_column(df, ['sleep', 'sleep_hours', 'avg_sleep'])
		exercise_col = find_column(df, ['exercise', 'exercise_hours', 'avg_exercise'])

		if not all([work_col, rest_col, sleep_col, exercise_col, target_col, occupation_col]):
			print('Could not compute work-life balance index — missing one of required columns:')
			print('work_col, rest_col, sleep_col, exercise_col, target_col, occupation_col ->',
				  work_col, rest_col, sleep_col, exercise_col, target_col, occupation_col)
		else:
			# Coerce numeric
			df['_w'] = pd.to_numeric(df[work_col], errors='coerce')
			df['_r'] = pd.to_numeric(df[rest_col], errors='coerce')
			df['_s'] = pd.to_numeric(df[sleep_col], errors='coerce')
			df['_e'] = pd.to_numeric(df[exercise_col], errors='coerce')

			# compute index: (rest + sleep + exercise) / (rest + sleep + exercise + work)
			df['work_life_balance_index'] = (
				df['_r'].fillna(0) + df['_s'].fillna(0) + df['_e'].fillna(0)
			) / (
				(df['_r'].fillna(0) + df['_s'].fillna(0) + df['_e'].fillna(0)) + df['_w'].fillna(0)
			)

			# replace infinities and NaN with NaN
			df['work_life_balance_index'].replace([np.inf, -np.inf], np.nan, inplace=True)

			# For each occupation, create a scatter+regression plot of index vs age_at_death
			occs = df[occupation_col].dropna().unique()
			wl_created = []
			for occ in occs:
				sub = df[df[occupation_col] == occ]
				sub = sub[[ 'work_life_balance_index', target_col]].dropna()
				if sub.shape[0] < 5:
					continue
				plt.figure(figsize=(6, 5))
				sns.regplot(x=sub['work_life_balance_index'], y=sub[target_col], scatter_kws={'s': 20, 'alpha': 0.6}, line_kws={'color': 'red'})
				disp_occ = str(occ).replace('_', ' ')
				plt.title(f'Work-life balance index vs {str(target_col).replace("_", " ")}: {disp_occ}')
				plt.xlabel('Work-life balance index')
				plt.ylabel(str(target_col).replace('_', ' '))
				plt.tight_layout()
				out = os.path.join(plots_dir, f'work_life_balance_index_vs_{safe_fname(target_col)}_by_{safe_fname(occ)}.png')
				if no_save:
					print('(no-save) would write', out)
				else:
					plt.savefig(out, dpi=dpi)
				plt.close()
				wl_created.append(out)

			if wl_created:
				print('Created work-life-balance index plots per occupation:')
				for p in wl_created:
					print('-', p)

	print('Created plots:')
	for p in [p for p in created if p]:
		print('-', p)


if __name__ == '__main__':
	main()

