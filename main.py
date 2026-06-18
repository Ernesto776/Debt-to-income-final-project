import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import create_and_get_files as file_utils
from debt_manager import DebtManager

COLOR_BG_DARK = "#1e1e24"
COLOR_BG_LIGHT = "#f8f9fa"
COLOR_PRIMARY = "#2b5c8f"
COLOR_SUCCESS = "#2a8a5e"
COLOR_ACCENT = "#d9534f"

class D2I_GUIapp:
    def __init__(self, root):
        self.debt_mgr = DebtManager(self)

        self.root = root
        self.root.title("Debt-to-Income Calculator")
        try:
            self.root.state('zoomed')
        except tk.TclError:
            root.wm_attributes("-zoomed", True)
        self.root.configure(bg=COLOR_BG_LIGHT)
    
        if "Segoe UI" in self.root.tk.call("font", "families"):
            self.font_family = "Segoe UI"
        else:
            self.font_family = "Arial"

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

        #Updates the GUI with set colors
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", font=(self.font_family, 10), background=COLOR_BG_LIGHT)
        self.style.configure("TLabel", background=COLOR_BG_LIGHT, foreground="#333333")
        self.style.configure("Header.TLabel", font=(self.font_family, 14, "bold"), background=COLOR_BG_LIGHT, foreground=COLOR_PRIMARY)
        self.style.configure("SidebarHeader.TLabel", font=(self.font_family, 14, "bold"), background=COLOR_BG_DARK, foreground="white")

        #Button style update
        self.style.configure("Primary.TButton", background=COLOR_PRIMARY, foreground="white", borderwidth=0, focuscolor="none")
        self.style.map("Primary.TButton", background=[("active", "#1f446b")])
        self.style.configure("Success.TButton", background=COLOR_SUCCESS, foreground="white", borderwidth=0)
        self.style.map("Success.TButton", background=[("active", "#1e6343")])
        self.style.configure("Danger.TButton", background=COLOR_ACCENT, foreground="white", borderwidth=0)
        self.style.map("Danger.TButton", background=[("active", "#b33c39")])
    
        self.setup_income()

    def create_input_fields(self, parent, label_text, is_dropdown=False, dropdown_var=None, dropdown_options=None, padding_bottom=12):
        ttk.Label(parent, text=label_text, font=(self.font_family, 9, "bold"), 
                background="white").pack(anchor="w", padx=25, pady=(5, 2))

        if is_dropdown:
            widget = ttk.OptionMenu(parent, dropdown_var, dropdown_options[0], *dropdown_options)
            widget.pack(fill=tk.X, padx=25, pady=(0, padding_bottom))
        else:
            widget = ttk.Entry(parent, font=(self.font_family, 10))
            widget.pack(fill=tk.X, padx=25, pady=(0, padding_bottom))
        return widget

    def setup_income(self):    
        """Left Panel"""
        left_panel = tk.Frame(self.root, bg="white", width=360, bd=1, relief=tk.SOLID)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        left_panel.pack_propagate(False)

        #Boundry line
        tk.Frame(self.root, bg="#e0e0e0", width=1).pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(left_panel, text="Financial Input", style="Header.TLabel",
                background="white").pack(pady=(20, 15), padx=25, anchor="w")

        #(Optional) Gross input
        self.gross_input = self.create_input_fields(left_panel, "(Optional) Gross Income:")
        self.gross_input.insert(0, "0")

        #Net income input
        self.net_input = self.create_input_fields(left_panel, "Insert net income:")

        #Income interval
        self.interval_input = tk.StringVar(value="Weekly")
        self.interval_dropdown = self.create_input_fields(
            left_panel, "Pay frequency interval:",
            is_dropdown=True, dropdown_var=self.interval_input,
            dropdown_options=["Weekly", "Bi-Weekly", "Monthly"]
        )

        #Debt input section
        tk.Frame(left_panel, bg="#eef2f5", height=2).pack(fill=tk.X, padx=20, pady=(5,5))

        ttk.Label(left_panel, text="Add debts:", style="Header.TLabel", 
                background="white").pack(anchor="w", padx=25, pady=(5,5))
        
        self.debt_name_input = self.create_input_fields(left_panel, "Name / label",
                padding_bottom=6)
        self.debt_amount_input = self.create_input_fields(left_panel, "Monthly debt value:",
                padding_bottom=6)
        
        self.debt_cat_var = tk.StringVar(value="Bills")
        self.debt_cat_dropdown = self.create_input_fields(
            left_panel, "Category classification:",
            is_dropdown=True, dropdown_var=self.debt_cat_var,
            dropdown_options=self.debt_mgr.categories,
            padding_bottom=6
        )

        ttk.Label(left_panel, text="Prioritization classification:", 
                font=(self.font_family, 9, 'bold'), background="white"
                ).pack(anchor="w", padx=25, pady=(4,2))
        
        btn_frame = tk.Frame(left_panel, bg="white")
        btn_frame.pack(fill=tk.X, padx=25, pady=(0,10))

        #Setup inline selector buttons
        button_config = [
            ("High priority", "!!! Critical", "#d9534f", (0, 4)),
            ("Medium priority", "!! Medium", "#f78605", 2),
            ("Low priority", "! Low", "#5cb85c", (2, 0))
        ]

        self.priority_buttons = {}

        for level, label, active_color, padding in button_config:
            #High is active first
            is_high = (level == "High priority")

            #Sets button color
            if is_high:
                bg_color = active_color
                fg_color = "white"
            else:
                bg_color = "#f5f5f5"
                fg_color = active_color

            btn = tk.Button(
                btn_frame, text=label, font=(self.font_family, 9, 'bold'),
                bg=bg_color, fg=fg_color, relief=tk.FLAT, bd=0)

            btn.config(command=lambda prio=level, b=btn: self.debt_mgr.set_priority(prio, b, self.priority_buttons))
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=padding, ipady=3)
            self.priority_buttons[level] = (btn, active_color)

        #Add debt buttons
        debt_btn_frame = tk.Frame(left_panel, bg="white")
        debt_btn_frame.pack(fill=tk.X, padx=20, pady=5)

        ttk.Button(debt_btn_frame, text="Add Debt", style="Success.TButton",
                command=lambda: self.debt_mgr.submit_debt(self.debt_name_input, 
                self.debt_amount_input, self.debt_cat_var)).pack(
                side=tk.LEFT, fill=tk.X, expand=True, padx=(4, 0))
        
        ttk.Button(debt_btn_frame, text="Undo Last Debt", style="Danger.TButton",
                command=self.debt_mgr.undo_debt).pack(side=tk.RIGHT, fill=tk.X, 
                expand=True, padx=(0, 4), pady=3)
    
        #The Debt listbox
        self.debt_listbox = tk.Listbox(left_panel, height=4, font=(self.font_family, 9), 
                bd=1, relief=tk.SOLID, highlightthickness=0, fg="#555555")
        self.debt_listbox.pack(fill=tk.X, padx=20, pady=5)

        #Storage buttons
        storage_frame = tk.Frame(left_panel, bg="white")
        storage_frame.pack(fill=tk.X, padx=20, pady=5)

        self.save_file = ttk.Button(storage_frame, text="Save File", 
                command=lambda: file_utils.save_file(self)
                )
        self.save_file.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,4))
        
        self.load_file = ttk.Button(storage_frame, text="Load File", 
                command=lambda: file_utils.load_file(self))
        self.load_file.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(4,0))

        """Right panel"""
        right_panel = tk.Frame(self.root, background=COLOR_BG_LIGHT)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        #Chart frame
        self.chart_frame = tk.Frame(right_panel, bg="white", bd=0)
        self.chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.placeholder_label = tk.Label(self.chart_frame, text="Insert information to have the data appear",
                font=(self.font_family, 11, "italic"), bg="white", fg="#888888")
        self.placeholder_label.pack(expand=True)
        
        #Dynamic sidebar frame
        sidebar = tk.Frame(right_panel, bg=COLOR_BG_DARK, width=280)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        sidebar.pack_propagate(False)

        #Breakdown inside the sidebar
        self.side_title = tk.Label(sidebar, text="Financial Breakdown", 
                font=(self.font_family, 14, "bold"), bg=COLOR_BG_DARK, fg="white")
        self.side_title.pack(pady=(25,15), padx=20, anchor="w")
        self.side_text = tk.Text(sidebar, font=("Courier New", 9), bg=COLOR_BG_DARK, 
                fg="White", bd=0, wrap=tk.WORD, highlightthickness=0)
        self.side_text.pack(fill=tk.BOTH, expand=True, padx=25, pady=(0, 20))
        self.update_sidebar("System standby", ["Waiting for user inputs"])

    def calculate_income(self):
        try:
            gross_income = float(self.gross_input.get() if self.gross_input.get() else 0)
            net_income = float(self.net_input.get())

            if net_income <= 0:
                messagebox.showerror("Value Error", "Income cannot be less than one.")
                return
            elif 0 < gross_income < net_income:
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
            self.financial_data['monthly_debt'] = sum(debt['amount'] for debt in self.financial_data['debt_collection'])
            self.financial_data['yearly_debt'] = (self.financial_data['monthly_debt'] * 12)

            if self.placeholder_label and self.placeholder_label.winfo_exists():
                self.placeholder_label.destroy()
                self.placeholder_label = None

            self.render_chart()
            self.update_sidebar("Overall Stats:", self.get_breakdown('all'))
        except ValueError:
            messagebox.showerror("Input Error", "Please put in the correct numbers")

    def render_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        net_income = self.financial_data['net_income']
        yearly_debt = self.financial_data['yearly_debt']
        remainder = max(0, net_income - yearly_debt)
        category_totals = self.debt_mgr.get_category_total()
        
        #label setup
        labels, sizes, colors = [], [], []
        theme_colors = ["#d9534f", "#f78605", "#5bc0de", "#5cb85c", "#777777"]

        for color, categ in enumerate (self.debt_mgr.categories):
            val = category_totals[categ]
            if val > 0:
                labels.append(categ)
                sizes.append(val)
                colors.append(theme_colors[color])

        if remainder >= 0 or not labels:
            labels.append('Savings/liquid')
            sizes.append(remainder)
            colors.append(COLOR_PRIMARY)

        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
        fig.patch.set_facecolor("white")

        wedges, _, _ = ax.pie(
            sizes, labels=labels, autopct='%1.1f%%',
            startangle=140, colors=colors,
            textprops={'fontname':self.font_family, 'fontsize':9, 'weight':'bold'},
            wedgeprops=dict(width=0.4, edgecolor='w', picker=True)
        )
        ax.set_title("Annual Finance tracker", fontname=self.font_family, fontsize=11, weight='bold', color="#444444")

        def hover_display(event):
            if event.inaxes != ax:
                return
            
            hover_detect = self.handle_wedge_hover(event, wedges, labels, fig)

            #Remove display if the cursor goes outside of range
            if not hover_detect:
                for wedge in wedges:
                    wedge.set_alpha(1.0)
                self.update_sidebar("Global Metrics", self.get_breakdown('all'))
                fig.canvas.draw_idle()
                
        fig.canvas.mpl_connect("motion_notify_event", hover_display)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def handle_wedge_hover(self, event, wedges, labels, fig):
        for i, wedge in enumerate(wedges):
            contained, _ = wedge.contains(event)
            if not contained:
                continue

            wedge.set_alpha(0.7)
            label_target = labels[i]

            if label_target == "Savings/liquid":
                self.update_sidebar(label_target, self.get_breakdown("liquid"))
            else:
                self.update_sidebar(
                    f"{label_target} Summary",
                    self.debt_mgr.get_category(label_target)
                )

            fig.canvas.draw_idle()
            return True
        return False

    def get_breakdown(self, scope):
        fd = self.financial_data
        rem = max(0, fd['net_income'] - fd['yearly_debt'])
        if fd['net_income'] > 0:
            dti = ((fd['monthly_debt'] / (fd['net_income'] / 12)) * 100 )
        else:
            dti = 0

        high_p, med_p, low_p = self.debt_mgr.get_priority_total()

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