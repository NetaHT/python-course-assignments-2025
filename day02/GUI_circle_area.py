import tkinter as tk
from tkinter import ttk
from circle_area import calculate_circle_area

class CircleAreaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Circle Area Calculator")
        
        # Create and set up the main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create the radius entry field
        ttk.Label(self.main_frame, text="Enter radius:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.radius_var = tk.StringVar()
        self.radius_entry = ttk.Entry(self.main_frame, textvariable=self.radius_var)
        self.radius_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Create the calculate button
        ttk.Button(self.main_frame, text="Calculate Area", command=self.calculate).grid(row=1, column=0, columnspan=2, pady=10)
        
        # Create the result label
        self.result_var = tk.StringVar()
        ttk.Label(self.main_frame, textvariable=self.result_var).grid(row=2, column=0, columnspan=2)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)

    def calculate(self):
        try:
            radius = float(self.radius_var.get())
            if radius <= 0:
                self.result_var.set("Please enter a positive number for radius")
                return
                
            area = calculate_circle_area(radius)
            self.result_var.set(f"The area is: {area} square units")
        except ValueError:
            self.result_var.set("Please enter a valid number")

def main():
    root = tk.Tk()
    app = CircleAreaGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
