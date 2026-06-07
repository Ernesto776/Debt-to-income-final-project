import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import create_and_get_files as file_utils

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
            ("Pay interval:", "interval", tk.OptionMenu)
        ]
    
        #Left Panel
        left_panel = tk.Frame(self.root, bg="#ffffff", width=360, bd=1, relief=tk.SOLID)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        left_panel.pack_propagate(False)

        """Income input Label in left panel"""
        tk.Label(left_panel, text="Financial Input", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)
        self.inputs = {}

        self.interval_input = tk.StringVar(value="Weekly")

        for label_text, key, widget_type in labels:
            tk.Label(left_panel, text=label_text, font=("Arial", 10), bg="#ffffff").pack(anchor="w", padx=20, pady=(5, 0))
            if widget_type == tk.Entry:
                self.inputs[key] = tk.Entry(left_panel, font=("Arial", 10))
                if key == "gross": self.inputs[key].insert(0, "0")
                self.inputs[key].pack(fill=tk.X, padx=20, pady=2)
            else:
                self.inputs[key] = tk.OptionMenu(left_panel, self.interval_input, "Weekly", "Bi-Weekly", "Monthly")
                self.inputs[key].pack(fill=tk.X, padx=20,pady=2)

        self.gross_input = self.inputs["gross"]
        self.net_input = self.inputs["net"]

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

        self.make_btn(left_panel, "Calculate and update chart", "#3498db", self.calculate_income, pady=10)
        self.make_btn(left_panel, "Undo last debt entry", "#7f8c8d", self.undo_debt)

        storage_frame = tk.Frame(left_panel, bg="#ffffff")
        storage_frame.pack(fill=tk.X, padx=20, pady=5)
        self.make_btn(storage_frame, "Save File", "#9b59b6", lambda: file_utils.save_file(self), tk.LEFT)
        self.make_btn(storage_frame, "Load File", "#f1c40f", lambda: file_utils.load_file(self), tk.RIGHT)

        #Right panel
        right_panel = tk.Frame(self.root, bg="#f4f4f6")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        """Chart frame in the right panel"""
        self.chart_frame = tk.Frame(right_panel, bg="#ffffff", bd=1, relief=tk.SOLID)
        self.chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        """Dynamic sidebar frame in the right panel"""
        sidebar = tk.Frame(right_panel, bg="#ffffff", width=280, bd=1, relief=tk.SOLID)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        sidebar.pack_propagate(False)

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
                multiplier = 24
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
            self.financial_data['yearly_debt'] = (self.financial_data['monthly_debt'] * 12)

            self.render_chart()
            self.update_sidebar("Overall Stats:", self.get_breakdown('all'))
        except ValueError:
            messagebox.showerror("Input Error", "Please put in the correct numbers")

    def render_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        net_income = self.financial_data['net_income']
        yearly_debt = self.financial_data['yearly_debt']
        remainder = net_income - yearly_debt

        #label setup
        labels = ['Total debt', 'Remaining money']
        sizes = [yearly_debt, max(0, remainder)]
        colors=['#c0392b', '#2ecc71']

        if remainder < 0:
            labels = ['Negative by: ']
            sizes = [yearly_debt]
            colors = ['#c0392b']

        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
        wedges, _, _ = ax.pie(
            sizes, labels=labels, autopct='%1.1f%%',
            startangle=140, colors=colors,
            wedgeprops=dict(width=0.4, edgecolor='w', picker=True)
        )
        ax.set_title("Annual Finance tracker")

        def hover_display(event):
            if event.inaxes == ax:
                for i, wedge in enumerate(wedges):
                    contained, _ = wedge.contains(event)
                    if contained:
                        wedge.set_alpha(0.7)
                        label_target = labels[i]
                        context = 'debt' if 'debt' in label_target else 'liquid'
                        self.update_sidebar(label_target, self.get_breakdown(context))
                        fig.canvas.draw_idle()
                        return
                
                #Remove display if the cursor goes outside of range
                for wedge in wedges:
                    wedge.set_alpha(1.0)
                self.update_sidebar("Global Metrics", self.get_breakdown('all'))
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect("motion_notify_event", hover_display)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def get_breakdown(self, scope):
        fd = self.financial_data
        rem = max(0, fd['net_income'] - fd['yearly_debt'])
        if fd['net_income'] > 0:
            dti = ((fd['monthly_debt'] / (fd['net_income'] / 12)) * 100 )
        else:
            dti = 0

        debt_breakdown = [
            "---DEBT BREAKDOWN---",
            f"Monthly debt: ${fd['monthly_debt']:.2f}",
            f"Annual Out:  ${fd['yearly_debt']:.2f}",
            f"DTI Ratio:   {dti:.2f}%\n"
        ]

        liquid_breakdown = ["--- INCOME ---"]
        if fd["gross_income"] > 0:
            liquid_breakdown.append(f"Gross Ann:   ${fd['gross_income']:.2f}")
            liquid_breakdown.append(f"Tax Paid:    ${fd['taxed_dollars']:.2f} ({fd['tax_percent']:.1f}%)")

        liquid_breakdown.append(f"Net Ann:     ${fd['net_income']:.2f}")
        liquid_breakdown.extend([
            "",
            "REMAINING SPENDING MONEY",

            f"Monthly:     ${rem/12:.2f}",
            f"Weekly:      ${rem/52:.2f}",
            f"Daily:       ${rem/365:.2f}"
        ])

        if scope == 'all':
            return debt_breakdown + [""] + liquid_breakdown
        elif scope == 'liquid':
            return liquid_breakdown
        else:
            return debt_breakdown
    
    def update_sidebar(self, head, text):
        self.side_title.config(text=head)
        self.side_text.config(state=tk.NORMAL)
        self.side_text.delete(1.0, tk.END)

        formatted_text = "\n".join(text)

        self.side_text.insert(tk.END, formatted_text)
        self.side_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = D2I_GUIapp(root)
    root.mainloop()