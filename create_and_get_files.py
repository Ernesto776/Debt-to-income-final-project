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
                loaded_data =json.load(f)

            app.financial_data.clear()
            app.financial_data.update(loaded_data)

            app.debt_listbox.delete(0, tk.END)
            p_indicators = {
                "High priority": "!!!",
                "Medium priority": "!!",
                "Low priority": "!"
            }
            for debt in app.financial_data.get('debt_collection', []): 
                name = debt.get('name', 'Unlabeled Liability')
                amount = debt.get('amount', 0.0)
                prio = debt.get('priority', 'Low priority')
                p_flag = p_indicators.get(prio, "!")
                app.debt_listbox.insert(tk.END, f"[{p_flag}] {name} : ${amount:.2f}/month")

            app.net_input.delete(0, tk.END)

            app.interval_input.set("Monthly")
            monthly_net = app.financial_data.get('net_income', 0.0) / 12
            app.net_input.insert(0, f"{monthly_net:.2f}")

            if 'gross_income' in app.financial_data:
                app.gross_input.delete(0, tk.END)
                monthly_gross = app.financial_data.get('gross_income', 0.0) / 12
                app.gross_input.insert(0, f"{monthly_gross:.2f}")

            app.calculate_income()

            #app.render_chart()
            #app.update_sidebar("Global Metrics", app.get_breakdown('all'))
        except Exception as file_not_found:
            messagebox.showerror("Error", f"Failed to load file: {file_not_found}")