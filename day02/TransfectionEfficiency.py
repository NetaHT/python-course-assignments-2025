#!/usr/bin/env python3

"""
TransfectionEfficiency.py

Updated to accept measured total cell count and GFP+ cell count on the day of experiment.

Inputs expected via CLI:
- --cell-type: S2 or BG3
- --total-cells: total cells measured on day of experiment (cells/ml)
- --gfp-cells: GFP+ cells measured on day of experiment (cells/ml)
- --days-since-transfection: days elapsed since transfection

Output:
- Estimated initial transfection percentage (on day 0), accounting for growth/doubling
- Current fraction of GFP+ cells in the population
- Generations elapsed and expected initial total cells

Assumptions:
- Doubling times (literature-average): S2 = 24 h, BG3 = 30 h
- One daughter cell inherits the plasmid at each division -> absolute GFP+ cell number approximately constant over divisions
"""

import argparse
from math import pow


class TransfectionEfficiencyCalculator:
    def __init__(self):
        # Doubling times in hours (literature averages)
        self.CELL_PROPERTIES = {
            'S2': {'doubling_time_hours': 24.0},
            'BG3': {'doubling_time_hours': 30.0}
        }

    def estimate_initial_efficiency(self, cell_type: str,
                                    total_cells_current: float,
                                    gfp_cells_current: float,
                                    days_since_transfection: float) -> dict:
        """
        Estimate initial transfection efficiency given current measurements.

        Returns dict with:
          - initial_efficiency_pct
          - current_efficiency_pct
          - generations
          - expected_initial_total_cells
          - doubling_time_hours
        """
        if cell_type not in self.CELL_PROPERTIES:
            raise ValueError(f"cell_type must be one of {list(self.CELL_PROPERTIES)}")
        if total_cells_current <= 0:
            raise ValueError("total_cells_current must be > 0")
        if gfp_cells_current < 0:
            raise ValueError("gfp_cells_current must be >= 0")
        if days_since_transfection < 0:
            raise ValueError("days_since_transfection must be >= 0")

        doubling = self.CELL_PROPERTIES[cell_type]['doubling_time_hours']
        hours = days_since_transfection * 24.0
        generations = hours / doubling if doubling > 0 else 0.0

        # Estimate initial total cells (before growth)
        expected_initial_total = total_cells_current / pow(2.0, generations)

        # Under the 'one daughter inherits plasmid' assumption the absolute number
        # of GFP+ cells stays approximately equal to the initial transfected cell number.
        initial_transfected_cells = gfp_cells_current

        initial_efficiency_pct = (initial_transfected_cells / expected_initial_total) * 100.0
        current_efficiency_pct = (gfp_cells_current / total_cells_current) * 100.0

        return {
            'initial_efficiency_pct': initial_efficiency_pct,
            'current_efficiency_pct': current_efficiency_pct,
            'generations': generations,
            'expected_initial_total_cells': expected_initial_total,
            'doubling_time_hours': doubling
        }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description='Estimate initial transfection efficiency from current measurements')
    p.add_argument('--cell-type', required=True, choices=['S2', 'BG3'], help='Cell type (S2 or BG3)')
    p.add_argument('--total-cells', required=True, type=float,
                   help='Total cells measured on day of experiment (cells/ml)')
    p.add_argument('--gfp-cells', required=True, type=float,
                   help='GFP+ cells measured on day of experiment (cells/ml)')
    p.add_argument('--days-since-transfection', required=True, type=float,
                   help='Days elapsed since transfection (can be fractional)')
    return p


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    calc = TransfectionEfficiencyCalculator()
    try:
        res = calc.estimate_initial_efficiency(
            cell_type=args.cell_type,
            total_cells_current=args.total_cells,
            gfp_cells_current=args.gfp_cells,
            days_since_transfection=args.days_since_transfection
        )
    except ValueError as e:
        print(f"Error: {e}")
        return 2

    print("\nTransfection Estimation")
    print(f"Cell type: {args.cell_type}")
    print(f"Doubling time: {res['doubling_time_hours']:.1f} h")
    print(f"Generations elapsed: {res['generations']:.2f}")
    print(f"Total cells (measured): {args.total_cells:,.2f} cells/ml")
    print(f"GFP+ cells (measured): {args.gfp_cells:,.2f} cells/ml")
    print(f"Estimated initial total cells (day 0): {res['expected_initial_total_cells']:,.2f} cells/ml")
    print(f"\nEstimated initial transfection efficiency: {res['initial_efficiency_pct']:.2f} %")
    print(f"Current fraction GFP+: {res['current_efficiency_pct']:.4f} %")

    # Alerts for abnormal values
    ALERT_LOW = 20.0   # percent
    ALERT_HIGH = 100.0 # percent

    if res['initial_efficiency_pct'] < ALERT_LOW:
        print("\nALERT: Estimated initial transfection efficiency is below 20%.")
        print("Consider optimizing transfection: increase DNA/reagent, check cell health, or adjust timing/temperature.")

    if res['initial_efficiency_pct'] > ALERT_HIGH:
        print("\n⚠️ ALERT: Estimated initial transfection efficiency exceeds 100%.")
        print("This is likely due to incorrect input values.")
        print("Please double-check your total cell count, GFP+ cell count, and time since transfection.")

    print("\nNotes: Assumes one daughter inherits the plasmid at each division (absolute GFP+ cell number approximately constant).\n")

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
