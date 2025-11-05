#this file creates a GUI to calculate the date 18 days before a given date

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class DateCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Last Date For Collection Calculator")
        
        # Create and set up the main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create the date entry fields
        ttk.Label(self.main_frame, text="Enter Date (DD/MM/YYYY):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.date_entry = ttk.Entry(self.main_frame, width=30)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Create the calculate button
        ttk.Button(self.main_frame, text="Calculate", command=self.calculate_date).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Create the result label
        self.result_var = tk.StringVar()
        ttk.Label(self.main_frame, textvariable=self.result_var).grid(row=2, column=0, columnspan=2, pady=5)
        
        # Set today's date as default
        today = datetime.now().strftime("%d/%m/%Y")
        self.date_entry.insert(0, today)

    def calculate_date(self):
        try:
            # Get the date from the entry field
            date_str = self.date_entry.get()
            input_date = datetime.strptime(date_str, "%d/%m/%Y")
            
            # Calculate date 18 days before
            result_date = input_date - timedelta(days=18)
            
            # Update the result label
            self.result_var.set(f"Result: {result_date.strftime('%d/%m/%Y')}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid date in DD/MM/YYYY format")

def main():
    root = tk.Tk()
    app = DateCalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()