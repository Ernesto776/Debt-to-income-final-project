financial_data = {
    'gross_income': 0,
    'net_income': 0,
    'debt_collection': [],
    'monthly_debt': 0,
    'yearly_debt': 0,
    'tax_percent': 0,
    'taxed_dollars': 0
}

def main_menu():
    global financial_data
    while True:
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

def enter_income():
    global financial_data
    while True:
        try:
            print(f"Your gross income is: {financial_data['gross_income']}")
            gross_income = input('(OPTIONAL) Please enter your gross income, "clear" to wipe all data, "back" to go back, otherwise enter "0": ').lower()
            if gross_income in ["clear", "reset", "delete"]:
                financial_data['gross_income'] = 0
                financial_data['net_income'] = 0
                financial_data['gross_income'] = 0
                print("Income data has been cleared.")
                continue
            elif gross_income == 'back':
                return
            print(f"Your net-income is: {financial_data['net_income']}")
            net_income = float(input("Please enter your net income: "))
            gross_income = float(gross_income)
            print(f"Your net income is: {net_income}")
            if gross_income > net_income and net_income > 0: 
                financial_data['tax_percent'] = ((gross_income - net_income) / gross_income) * 100
                financial_data['taxed_dollars'] = gross_income - net_income
                print(f"your gross income is: {gross_income:.2f} and your net income is: {net_income:.2f}")
                print(f"Your tax percentage is: {financial_data['tax_percent']:.2f}% and the amount of taxed dollars is: ${financial_data['taxed_dollars']:.2f}!")
                financial_data['gross_income'] = gross_income
                financial_data['net_income'] = net_income
            elif gross_income == 0 and net_income > 0:
                financial_data['net_income'] = net_income
                print(f"Your net-income is {net_income:.2f}")
            elif gross_income > 1 and gross_income < net_income:
                print("Gross income must be greater than net income. Please try again.")
                continue
            else:
                print("0 or Negative values are not allowed. Please try again.")
                continue
            while True:
                time_interval = input("Enter time interval (weekly, bi-weekly, monthly or yearly: ").lower()
                if time_interval == 'weekly':
                    financial_data['gross_income'] *= 52
                    financial_data['net_income'] *= 52
                    return
                elif time_interval == 'bi-weekly' or time_interval == 'biweekly':
                    financial_data['gross_income'] *= 26
                    financial_data['net_income'] *= 26
                    return
                elif time_interval == 'monthly':
                    financial_data['gross_income'] *= 12
                    financial_data['net_income'] *= 12
                    return
                elif time_interval == 'yearly' or time_interval == 'annually':
                    return
                else:
                    print("Invalid time interval. Please try again.")
                    continue
        except ValueError:
            print("Invalid input. Please enter numeric values for income.")
            continue

def enter_debt():
    global financial_data
    while True:
        user_command = input(f'Enter monthly debt amount or “finish” to finish or “undo” to remove last input: ').lower()
        if user_command == 'finish':
            break
        elif user_command == 'undo' or user_command == 'remove' or user_command == 'delete':
            if financial_data['debt_collection']:
                removed_debt = financial_data['debt_collection'].pop()
                print(f"Removed last debt entry: ${removed_debt:.2f}")
            else:
                print("No debt entries to remove.")
            continue
        else:
            try:
                debt_amount = float(user_command)
                if debt_amount <= 0:
                    print("Please enter a positive value for debt.")
                    continue
                financial_data['debt_collection'].append(debt_amount)
                print(f"Added debt entry: ${debt_amount:.2f}")
            except ValueError:
                print("Invalid input. Please enter a numeric value for debt, 'finish', or 'undo'.")
                continue
    financial_data['monthly_debt'] = sum(financial_data['debt_collection'])
    financial_data['yearly_debt'] = financial_data['monthly_debt'] * 12
    print(f"Your total monthly debt is: ${financial_data['monthly_debt']:.2f} and your total yearly debt is: ${financial_data['yearly_debt']:.2f}")

def check_ito_ratio():
    global financial_data
    if financial_data['net_income'] == 0:
        print("Please enter your income first.")
        return
    elif financial_data['monthly_debt'] == 0:
        print("Please enter your debt first.")
        return
    dti_ratio = (financial_data['monthly_debt'] / (financial_data['net_income'] / 12)) * 100
    print("Heres a guideline to help you spend available money without going into debt:")
    money_after_expenses = financial_data['net_income'] - financial_data['yearly_debt']
    if financial_data['gross_income'] > 0:
        print("Annual gross income: ${:.2f}".format(financial_data['gross_income']))
        print("Annual net income: ${:.2f}".format(financial_data['net_income']))
        print("tax percentage: {:.2f}%".format(financial_data['tax_percent']))
        print("taxed dollars: ${:.2f}".format(financial_data['taxed_dollars']))
    else:
        print("Annual net income: ${:.2f}".format(financial_data['net_income']))
    print("Annual debt: ${:.2f}".format(financial_data['yearly_debt']))
    print("Monthly debt: ${:.2f}".format(financial_data['monthly_debt']))
    print(f"Your Debt-to-Income (DTI) ratio is: {dti_ratio:.2f}%")
    print("Money left after expenses: ${:.2f}".format(money_after_expenses))
    print("Money left after expenses per month: ${:.2f}".format(money_after_expenses / 12))
    print("Money left after expenses per week: ${:.2f}".format(money_after_expenses / 52))
    print("Money left after expenses per day: ${:.2f}".format(money_after_expenses / 365))
    if money_after_expenses < 0:
        print("Woah! You are spending more than you make! Either reduce your expenses or consider getting another job.")
    print("Thank you and I hope this was able to help you! press any button to return to the main menu.")
    input()
    
main_menu()