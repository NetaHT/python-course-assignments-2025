#!/usr/bin/env python3

"""
TransfectionEfficiencyGUI.py

Graphical interface for Transfection Efficiency Calculator.

Uses TransfectionEfficiencyCalculator from TransfectionEfficiency.py.
Prompts user for inputs and displays calculated efficiency and alerts.

Requirements:
- Python 3.x
- Tkinter (usually included with Python)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from TransfectionEfficiency import TransfectionEfficiencyCalculator


class TransfectionEfficiencyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🧬 Transfection Efficiency Calculator")
        self.geometry("500x500")
        self.resizable(False, False)
        self.configure(bg="#f8f8f8")

        # Calculator instance
        self.calc = TransfectionEfficiencyCalculator()

        # GUI Layout
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text="Transfection Efficiency Calculator", font=("Arial", 16, "bold"), bg="#f8f8f8")
        title.pack(pady=10)

        frame = ttk.Frame(self, padding=20)
        frame.pack(padx=10, pady=10, fill="x")

        # --- Input Fields ---
        self.cell_type_var = tk.StringVar(value="S2")
        ttk.Label(frame, text="Cell type:").grid(row=0, column=0, sticky="w", pady=5)
        ttk.OptionMenu(frame, self.cell_type_var, "S2", "S2", "BG3").grid(row=0, column=1, sticky="ew", pady=5)

        self.total_cells_var = tk.StringVar()
        ttk.Label(frame, text="Total cells (cells/ml):").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(frame, textvariable=self.total_cells_var).grid(row=1, column=1, sticky="ew", pady=5)

        self.gfp_cells_var = tk.StringVar()
        ttk.Label(frame, text="GFP+ cells (cells/ml):").grid(row=2, column=0, sticky="w", pady=5)
        ttk.Entry(frame, textvariable=self.gfp_cells_var).grid(row=2, column=1, sticky="ew", pady=5)

        self.days_var = tk.StringVar()
        ttk.Label(frame, text="Days since transfection:").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Entry(frame, textvariable=self.days_var).grid(row=3, column=1, sticky="ew", pady=5)

        frame.columnconfigure(1, weight=1)

        # --- Buttons ---
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Calculate", command=self.calculate).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_fields).pack(side="left", padx=5)

        # --- Results Display ---
        self.result_box = tk.Text(self, height=12, width=55, wrap="word", state="disabled", bg="#f4f4f4")
        self.result_box.pack(padx=10, pady=10)

    def calculate(self):
        try:
            cell_type = self.cell_type_var.get().strip()
            total_cells = float(self.total_cells_var.get())
            gfp_cells = float(self.gfp_cells_var.get())
            days = float(self.days_var.get())

            result = self.calc.estimate_initial_efficiency(
                cell_type=cell_type,
                total_cells_current=total_cells,
                gfp_cells_current=gfp_cells,
                days_since_transfection=days
            )

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return
        except Exception:
            messagebox.showerror("Error", "An unexpected error occurred. Please check your input values.")
            return

        # --- Prepare results text ---
        text = []
        text.append(f"📊 Results for {cell_type} cells\n")
        text.append(f"Doubling time: {result['doubling_time_hours']:.1f} h")
        text.append(f"Generations elapsed: {result['generations']:.2f}")
        text.append(f"Measured total cells: {total_cells:,.2f} cells/ml")
        text.append(f"Measured GFP+ cells: {gfp_cells:,.2f} cells/ml")
        text.append(f"Estimated initial total cells (day 0): {result['expected_initial_total_cells']:,.2f} cells/ml\n")
        text.append(f"Estimated initial transfection efficiency: {result['initial_efficiency_pct']:.2f} %")
        text.append(f"Current GFP+ fraction: {result['current_efficiency_pct']:.4f} %\n")

        # --- Alerts ---
        alerts = []
        if result['initial_efficiency_pct'] < 20.0:
            alerts.append("⚠️ Efficiency below 20% — consider optimizing transfection (DNA/reagent ratio, cell health, etc.).")
        if result['initial_efficiency_pct'] > 100.0:
            alerts.append("⚠️ Efficiency exceeds 100% — likely due to incorrect inputs. Please recheck your measurements.")

        if alerts:
            text.append("\n".join(alerts))

        text.append("\nAssumption: One daughter inherits the plasmid; absolute GFP+ cell count ≈ constant.\n")

        # --- Display in result box ---
        self.result_box.configure(state="normal")
        self.result_box.delete(1.0, tk.END)
        self.result_box.insert(tk.END, "\n".join(text))
        self.result_box.configure(state="disabled")

    def clear_fields(self):
        self.total_cells_var.set("")
        self.gfp_cells_var.set("")
        self.days_var.set("")
        self.result_box.configure(state="normal")
        self.result_box.delete(1.0, tk.END)
        self.result_box.configure(state="disabled")


if __name__ == "__main__":
    app = TransfectionEfficiencyApp()
    app.mainloop()
