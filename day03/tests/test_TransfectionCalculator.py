import sys, os
import pytest

# Ensure Python can find the main module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from TransfectionEfficiency_BuisnessLogic import TransfectionEfficiencyCalculator


def test_estimate_efficiency_basic():
    calc = TransfectionEfficiencyCalculator()
    result = calc.estimate_initial_efficiency(
        cell_type='S2',
        total_cells_current=1e6,
        gfp_cells_current=1e5,
        days_since_transfection=2
    )

    # Basic sanity checks
    assert isinstance(result, dict)
    assert 'initial_efficiency_pct' in result
    assert 'current_efficiency_pct' in result
    assert result['current_efficiency_pct'] == pytest.approx(10.0, rel=1e-3)
    assert result['initial_efficiency_pct'] > result['current_efficiency_pct']
    assert result['generations'] > 0


def test_invalid_cell_type():
    calc = TransfectionEfficiencyCalculator()
    with pytest.raises(ValueError, match="cell_type must be one of"):
        calc.estimate_initial_efficiency('HeLa', 1e6, 1e5, 1)


def test_negative_total_cells():
    calc = TransfectionEfficiencyCalculator()
    with pytest.raises(ValueError, match="total_cells_current must be > 0"):
        calc.estimate_initial_efficiency('S2', -1, 100, 1)


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
