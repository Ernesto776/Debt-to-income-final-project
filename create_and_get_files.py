import tkinter as tk
from tkinter import messagebox, filedialog
import json

def save_file(self):
    path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if path: json.dump(self.financial_data, open(path, 'w'), indent=4)

def load_file(self):
    path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if path:
        try:
            self.financial_data.update(json.load(open(path,'r')))
            self.debt_listbox.delete(0, tk.END)
            for d in self.financial_data['debt_collection']: self.debt_listbox.insert(tk.END, f"${d:.2f} / mo")
            self.render_chart()
            self.update_sidebar("Global Metrics", self.get_breakdown('all'))
        except Exception as file_not_found:
            messagebox.showerror("Error", f"Failed to load file: {file_not_found}")