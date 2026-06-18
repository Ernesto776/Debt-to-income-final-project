import tkinter as tk
from tkinter import ttk, messagebox

class DebtManager:
    def __init__(self, app):
        self.app = app
        self.categories = [
            'Bills', 
            'Transportation', 
            'Entertainment', 
            'Food/Restaurants', 
            'Subscriptions',
            'Pets',
            'Money Investments',
        ]
        self.selected_priority = "High priority"

    def set_priority(self, level, target_btn, priority_buttons):
        self.selected_priority = level
            
        for k, (btn_object, color) in priority_buttons.items():
            if btn_object == target_btn:
                btn_object.config(bg=color, fg="white")
            else:
                btn_object.config(bg="#f5f5f5", fg=color)

    def submit_debt(self, name_entry, value_entry, cat_var):
        try:
            name = name_entry.get().strip() or "Unlabeled Liability"
            amount = float(value_entry.get())

            if amount <= 0:
                raise ValueError
                
            new_debt = {
                'name' : name,
                'amount' : amount,
                'category' : cat_var.get(),
                'priority' : self.selected_priority
            }
            self.app.financial_data['debt_collection'].append(new_debt)

            #Cleanly formats the priority indicators
            p_indicator = {
                "High priority": "!!!", 
                "Medium priority": "!!",
                "Low priority": "!"
            }
            p_flag = p_indicator.get(self.selected_priority, "!")

            self.app.debt_listbox.insert(tk.END, f"{p_flag} {name} : ${amount:.2f}/mo")
            
            #Cleans the entry every submission
            name_entry.delete(0, tk.END)
            value_entry.delete(0, tk.END)

            self.app.calculate_income()
        except ValueError:
            messagebox.showerror("Validation Error", "Provide a valid asset number")

    def undo_debt(self):
        if self.app.financial_data['debt_collection']:
            self.app.financial_data['debt_collection'].pop()
            self.app.debt_listbox.delete(tk.END)
            self.app.calculate_income()
        else:
            messagebox.showwarning("Undo debt error", "There are no debts to remove.")

    def add_debt_from_filter(self, key, value):
        return sum(debt['amount'] for debt in self.app.financial_data['debt_collection'] if debt.get(key) == value)
    
    def get_category_total(self):
        #Returns as an annual total
        return {cat: self.add_debt_from_filter('category', cat) * 12 for cat in self.categories}

    def get_priority_total(self):
        high_priority = self.add_debt_from_filter('priority', 'High priority')
        medium_priority = self.add_debt_from_filter('priority', 'Medium priority')
        low_priority = self.add_debt_from_filter('priority', 'Low priority')
        return high_priority, medium_priority, low_priority
    
    def get_category(self, category_name):
        lines = [f"{category_name.upper()} List"]
        matching = [debt for debt in self.app.financial_data['debt_collection'] 
                if debt.get('category') == category_name]

        high_pri_sum = 0.0
        med_pri_sum = 0.0
        low_pri_sum = 0.0

        for debt in matching:
            if debt.get('priority') == 'High priority':
                pri_tag = "!!!"
                high_pri_sum += debt['amount']
            elif debt.get('priority') == 'Medium priority':
                pri_tag = "!!"
                med_pri_sum += debt['amount']
            else:
                pri_tag = "!"
                low_pri_sum += debt['amount']
            lines.append(f"{pri_tag}{debt['name']}: ${debt['amount']:.2f}/month")

        lines.extend([
            "",
            "Priority breakdown:",
            f"High Priority: ${high_pri_sum:.2f}",
            f"Medium Priority: ${med_pri_sum:.2f}",
            f"Low priority: ${low_pri_sum:.2f}"
        ])
        return lines