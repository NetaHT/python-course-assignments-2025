# fly_recombination_gui.py
import tkinter as tk
from tkinter import messagebox
from FlyRecombination_BL import compute_genetic_distance

def calculate():
    gene1 = entry_gene1.get().strip()
    gene2 = entry_gene2.get().strip()
    if not gene1 or not gene2:
        messagebox.showerror("Error", "Please enter both FlyBase IDs")
        return
    try:
        result = compute_genetic_distance(gene1, gene2)
        output_text = ""
        if not result["same_chromosome"]:
            output_text += (f"The genes are on different chromosomes:\n"
                            f" - {gene1}: {result['chromosomes'][0]}\n"
                            f" - {gene2}: {result['chromosomes'][1]}\n"
                            f"Recombination rate is approximately 50%.\n")
        else:
            output_text += (f"Genes are on the same chromosome ({result['chromosomes'][0]}).\n"
                            f"Distance: {result['distance_bp']:,} bp ≈ {result['distance_cM']:.2f} cM\n"
                            f"Estimated recombination rate: {result['recomb_rate']*100:.2f}%\n")
            if result["warnings"]:
                output_text += "\n".join([f"⚠ {w}" for w in result["warnings"]])

        text_output.config(state="normal")
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, output_text)
        text_output.config(state="disabled")

    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("Drosophila Gene Distance and Recombination Rate Calculator")

tk.Label(root, text="FlyBase ID/ Gene name 1:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.Label(root, text="FlyBase ID/ Gene name 2:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

entry_gene1 = tk.Entry(root)
entry_gene2 = tk.Entry(root)
entry_gene1.grid(row=0, column=1, padx=5, pady=5)
entry_gene2.grid(row=1, column=1, padx=5, pady=5)

tk.Button(root, text="Calculate", command=calculate).grid(row=2, column=0, columnspan=2, pady=10)

text_output = tk.Text(root, width=50, height=10, state="disabled")
text_output.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
