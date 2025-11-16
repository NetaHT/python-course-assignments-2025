import typer
from math import pow

app = typer.Typer()

CELL_PROPERTIES = {'S2': 24.0, 'BG3': 30.0}

def estimate_initial_efficiency(cell_type: str, total_cells: float, gfp_cells: float, days: float):
    doubling = CELL_PROPERTIES[cell_type]
    generations = days * 24.0 / doubling
    initial_total = total_cells / pow(2.0, generations)
    initial_eff = gfp_cells / initial_total * 100
    current_eff = gfp_cells / total_cells * 100
    return initial_eff, current_eff, generations

@app.command()
def main(cell_type: str, total_cells: float, gfp_cells: float, days: float):
    init, current, gens = estimate_initial_efficiency(cell_type, total_cells, gfp_cells, days)
    typer.echo(f"Initial efficiency: {init:.2f}%  (after {gens:.2f} generations)")
    typer.echo(f"Current efficiency: {current:.2f}%")

if __name__ == "__main__":
    app()
