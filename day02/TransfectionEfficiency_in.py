#!/usr/bin/env python3

"""
TransfectionEfficiency_in.py

Interactive wrapper for TransfectionEfficiency calculator.
Supports both command line arguments and interactive input mode.
"""

import argparse
import sys
from TransfectionEfficiency import TransfectionEfficiencyCalculator

def get_interactive_input():
    """Get experiment parameters through interactive prompts"""
    print("\nTransfection Efficiency Calculator")
    print("=================================")
    
    # Get cell type
    while True:
        cell_type = input("\nEnter cell type (S2 or BG3): ").strip().upper()
        if cell_type in ['S2', 'BG3']:
            break
        print("Error: Please enter either S2 or BG3")
    
    # Get total cells with validation
    while True:
        try:
            total_cells = float(input("\nEnter total cell count (cells/ml): "))
            if total_cells <= 0:
                raise ValueError("Cell count must be positive")
            break
        except ValueError as e:
            print(f"Error: {str(e)}")
    
    # Get GFP+ cells with validation
    while True:
        try:
            gfp_cells = float(input("\nEnter GFP+ cell count (cells/ml): "))
            if gfp_cells < 0:
                raise ValueError("GFP+ count cannot be negative")
            if gfp_cells > total_cells:
                raise ValueError("GFP+ cells cannot exceed total cells")
            break
        except ValueError as e:
            print(f"Error: {str(e)}")
    
    # Get days since transfection
    while True:
        try:
            days = float(input("\nEnter days since transfection: "))
            if days < 0:
                raise ValueError("Days cannot be negative")
            break
        except ValueError as e:
            print(f"Error: {str(e)}")
    
    return {
        'cell_type': cell_type,
        'total_cells': total_cells,
        'gfp_cells': gfp_cells,
        'days': days
    }

def print_results(results):
    """Print calculator results with formatting"""
    print("\nResults:")
    print("========")
    print(f"Initial transfection efficiency: {results['initial_efficiency_pct']:.1f}%")
    print(f"Current GFP+ percentage: {results['current_efficiency_pct']:.1f}%")
    print(f"Cell generations: {results['generations']:.1f}")
    print(f"Estimated initial total cells: {results['expected_initial_total_cells']:.0f}")
    
     # Alerts for abnormal values
    ALERT_LOW = 20.0   # percent
    ALERT_HIGH = 100.0 # percent

    if results['initial_efficiency_pct'] < ALERT_LOW:
        print("\nALERT: Estimated initial transfection efficiency is below 20%.")
        print("Consider optimizing transfection: increase DNA/reagent, check cell health, or adjust timing/temperature.")

    if results['initial_efficiency_pct'] > ALERT_HIGH:
        print("\n⚠️ ALERT: Estimated initial transfection efficiency exceeds 100%.")
        print("This is likely due to incorrect input values.")
        print("Please double-check your total cell count, GFP+ cell count, and time since transfection.")

def build_parser():
    """Build argument parser for command line use"""
    p = argparse.ArgumentParser(
        description='Calculate transfection efficiency (interactive or CLI mode)'
    )
    p.add_argument('--cell-type', choices=['S2', 'BG3'],
                   help='Cell type (S2 or BG3)')
    p.add_argument('--total-cells', type=float,
                   help='Total cells measured (cells/ml)')
    p.add_argument('--gfp-cells', type=float,
                   help='GFP+ cells measured (cells/ml)')
    p.add_argument('--days-since-transfection', type=float,
                   help='Days elapsed since transfection')
    return p

def main(argv=None):
    # Parse any command line arguments
    parser = build_parser()
    args = parser.parse_args(argv)
    
    # Check if any arguments were provided
    if any(vars(args).values()):
        # Validate that all required args are present if any were given
        missing = [arg for arg, val in vars(args).items() if val is None]
        if missing:
            parser.error(f"Missing required arguments: {', '.join(missing)}")
        params = {
            'cell_type': args.cell_type,
            'total_cells': args.total_cells,
            'gfp_cells': args.gfp_cells,
            'days': args.days_since_transfection
        }
    else:
        # No args provided, use interactive mode
        params = get_interactive_input()
    
    # Calculate results
    calc = TransfectionEfficiencyCalculator()
    try:
        results = calc.estimate_initial_efficiency(
            params['cell_type'],
            params['total_cells'],
            params['gfp_cells'],
            params['days']
        )
        print_results(results)
        return 0
    except ValueError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())