#!/usr/bin/env python3
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