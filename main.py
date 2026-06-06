import tkinter as tk
from tkinter import messagebox, filedialog
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class D2I_GUIapp:
    def __init__(self, root):
        self.root = root
        self.root.title("Debt-to-Income Calculator")
        self.root.geometry("1050x600")
        self.root.configure(bg="#f4f4f6")

        #Variables to hold all financial data
        self.financial_data = {
            'gross_income': 0.0,
            'net_income': 0.0,
            'debt_collection': [],
            'monthly_debt': 0.0,
            'yearly_debt': 0.0,
            'tax_percent': 0.0,
            'taxed_dollars': 0.0
        }
        self.setup_income()

    def make_btn(self, parent, text, bg, cmd, side=None, **kwargs):
        button = tk.Button(parent, text=text, bg=bg, fg="white", command=cmd, font=("Arial", 10))
        if bg != "#f1c40f":
            bg = "black"
            button.configure(bg=bg)
        button.pack(side=side, fill=tk.X, expand=True, padx=2, **kwargs)
        return button

    def setup_income(self):
        labels = [
            ("(Optional) Gross Income:", "gross", tk.Entry),
            ("Net Income:", "net", tk.Entry),
            ("Pay interval:", "interval", tk.Entry)
        ]
    
        #Left Panel
        left_panel = tk.Frame(self.root, bg="#ffffff", width=360, bd=1, relief=tk.SOLID)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        left_panel.pack_propagate(False)

        """Income input Label in left panel"""
        tk.Label(left_panel, text="Financial Input", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

        self.gross_input, self.net_input, self.interval_input = self.inputs["gross"], self.inputs["net"], self.inputs.get("interval_menu").cget("textvariable")

        self.inputs = {}
        for label_text, key, widget_type in labels:
            tk.Label(left_panel, text=label_text, font=("Arial", 10), bg="#ffffff").pack(anchor="w", padx=20, pady=(5, 0))
            if widget_type == tk.Entry:
                self.inputs[key] = tk.Entry(left_panel, font=("Arial", 10))
                if key == "gross": self.inputs[key].insert(0, "0")
            else:
                self.inputs[key] = tk.StringVar(value="Monthly")
                self.inputs[key + "_menu"] = tk.OptionMenu(left_panel, self.inputs[key], "Weekly", "Bi-Weekly", "Monthly")
                self.inputs[key] = self.inputs[key + "_menu"]
            self.inputs[key].pack(fill=tk.X, padx=20, pady=2)

        """Debt input section in left panel"""
        tk.Label(left_panel, text="Add Monthly Debt:", font=("Arial", 9), bg="#ffffff").pack(anchor="w", padx=20, pady=(10,0))
        self.debt_input = tk.Entry(left_panel, font=("Arial", 10))
        self.debt_input.pack(fill=tk.X, padx=20, pady=2)

        """Add debt button in left panel"""
        debt_btn_frame = tk.Frame(left_panel, bg="#ffffff")
        debt_btn_frame.pack(fill=tk.X, padx=20, pady=5)
        self.make_btn(debt_btn_frame, "Add Debt", "#2ecc71", self.add_debt, tk.LEFT)
        self.make_btn(debt_btn_frame, "Undo Last Debt", "#e74c3c", self.undo_debt, tk.RIGHT)

        self.debt_listbox = tk.Listbox(left_panel, height=4, font=("Arial", 9))
        self.debt_listbox.pack(fill=tk.X, padx=20, pady=5)

        self.make_btn(left_panel, "Calculate and update chart", "#3498db", self.process_calculations, pady=10)
        self.make_btn(left_panel, "Undo last debt entry", "#7f8c8d", self.undo_debt)

        #Right panel
        right_panel = tk.Frame(self.root, bg="#f4f4f6")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        """Chart frame in the right panel"""
        self.chart_frame = tk.Frame(right_panel, bg="#ffffff", bd=1, relief=tk.SOLID)
        self.chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        """Dynamic sidebar frame in the right panel"""
        sidebar = tk.Frame(right_panel, bg="#ffffff")
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        sidebar.pack.propagate(False)

        """Breakdown inside the sidebar"""
        self.side_title = tk.Label(sidebar, text="Financial Breakdown", font=("Arial", 14, "bold"), bg="#ffffff")
        self.side_title.pack(pady=10)
        self.side_text = tk.Text(sidebar, font=("Courier", 9), bg="#ffffff", bd=0, wrap=tk.WORD)
        self.side_text.pack(fill=tk.BOTH, expand=True, padx=10)

    def add_debt(self):
        try:
            debt_amount = float(self.debt_input.get())
            if debt_amount <= 0:
                raise ValueError
            self.financial_data['debt_collection'].append(debt_amount)
            self.debt_listbox.insert(tk.END, f"${debt_amount:.2f} / month")
            self.debt_input.delete(0, tk.END)
        except ValueError:
            # Handle non-numeric input for debt with an error message
            messagebox.showerror("Error", "Enter a valid positive number for debt.")            

    def undo_debt(self):
        if self.financial_data['debt_collection']:
            self.financial_data['debt_collection'].pop()
            self.debt_listbox.delete(tk.END)
        else:
            messagebox.showwarning("There are debts to remove.")

    #Clear debt
    
    def calculate_income(self):
        try:
            gross_income = float(self.gross_input.get() if self.gross_input.get() else 0)
            net_income = float(self.net_input.get())

            if net_income <= 0:
                messagebox.showerror("Value Error", "Income cannot be less than one.")
                return
            elif gross_income < net_income and gross_income > 0:
                messagebox.showerror("Value Error", "Gross income cannot be less than net income")
                return
            
            interval = self.interval_input.get()
            if interval == "Weekly":
                multiplier = 52
            elif interval == "Bi-Weekly":
                multiplier = 26
            else:
                multiplier = 12

            annual_gross = (gross_income * multiplier)
            annual_net = (net_income * multiplier)

            if annual_gross > annual_net:
                self.financial_data['tax_percent'] = (((annual_gross - annual_net) / annual_gross) * 100)
                self.financial_data['taxed_dollars'] = (annual_gross - annual_net)
            else:
                self.financial_data['tax_percent'] = 0.0
                self.financial_data['taxed_dollars'] = 0.0

                self.financial_data['gross_income'] = annual_gross
                self.financial_data['net_income'] = annual_net
                self.financial_data['monthly_debt'] = sum(self.financial_data['debt_collection'])
                self.financial_data['yearly_debt'] = (self.financial_data['monthyl_debt'] * 12)

                self.render_chart()
                self.update_sidebar_display("Overall Stats:", self.generate_breakdown_string('all'))
        except ValueError:
            messagebox.showerror("Input Error", "Please put in the correct numbers")

"""
def main_menu():
    global financial_data
    while True:
        # Display main menu options and get user choice
        print("Welcome to the Main Menu")
        print("1. Enter Income")
        print("2. Enter Debt")
        print("3. Check Income-to-Expense Ratio")
        print("4. Exit")

        choice = input("Please select an option: ")

        if choice == '1':
            enter_income()
        elif choice == '2':
            enter_debt()
        elif choice == '3':
            check_ito_ratio()
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def check_ito_ratio():
    global financial_data
    if financial_data['net_income'] == 0:
        # If net income is zero, prompt user to enter income first
        print("Please enter your income first.")
        return
    elif financial_data['monthly_debt'] == 0:
        # If monthly debt is zero, prompt user to enter debt first
        print("Please enter your debt first.")
        return
    dti_ratio = (financial_data['monthly_debt'] / (financial_data['net_income'] / 12)) * 100
    print("Heres a guideline to help you spend available money without going into debt:")
    money_after_expenses = financial_data['net_income'] - financial_data['yearly_debt']
    if financial_data['gross_income'] > 0:
        # If gross income is provided, display gross income and tax details
        print("Annual gross income: ${:.2f}".format(financial_data['gross_income']))
        print("Annual net income: ${:.2f}".format(financial_data['net_income']))
        print("tax percentage: {:.2f}%".format(financial_data['tax_percent']))
        print("taxed dollars: ${:.2f}".format(financial_data['taxed_dollars']))
    else:
        # If gross income is not provided, only display net income
        print("Annual net income: ${:.2f}".format(financial_data['net_income']))
    # Display remaining financial details and DTI ratio
    print("Annual debt: ${:.2f}".format(financial_data['yearly_debt']))
    print("Monthly debt: ${:.2f}".format(financial_data['monthly_debt']))
    print(f"Your Debt-to-Income (DTI) ratio is: {dti_ratio:.2f}%")
    print("Money left after expenses: ${:.2f}".format(money_after_expenses))
    print("Money left after expenses per month: ${:.2f}".format(money_after_expenses / 12))
    print("Money left after expenses per week: ${:.2f}".format(money_after_expenses / 52))
    print("Money left after expenses per day: ${:.2f}".format(money_after_expenses / 365))
    if money_after_expenses < 0:
        # Warn user if they are spending more than they make
        print("Woah! You are spending more than you make! Either reduce your expenses or consider getting another job.")
    print("Thank you and I hope this was able to help you! press any button to return to the main menu.")
    input()
"""

if __name__ == "__main__":
    tk.Tk()
    D2I_GUIapp(tk.Tk()).mainloop()
#main_menu()