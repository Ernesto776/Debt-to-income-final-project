import tkinter as tk
from tkinter import messagebox, filedialog
import json

def save_file(app):
    path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if path: 
        with open(path, 'w') as f:
            json.dump(app.financial_data, f, indent=4)
        messagebox.showinfo("Success", "Data saved successfully!")

def load_file(app):
    path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if path:
        try:
            with open(path, 'r') as f:
                app.financial_data.update(json.load(f))

            app.debt_listbox.delete(0, tk.END)
            for d in app.financial_data['debt_collection']: 
                app.debt_listbox.insert(tk.END, f"${d:.2f} / month")

            app.net_input.delete(0, tk.END)
            app.net_input.insert(0, str(app.financial_data['net_income'] / 12))

            app.interval_input.set("Weekly")

            app.render_chart()
            app.update_sidebar("Global Metrics", app.get_breakdown('all'))
        except Exception as file_not_found:
            messagebox.showerror("Error", f"Failed to load file: {file_not_found}")