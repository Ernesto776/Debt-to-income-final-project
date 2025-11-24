def main_menu():
    print("Welcome to the Main Menu")
    print("1. Enter Income")
    print("2. Enter Debt")
    print("3. Check Debt-to-Income Ratio")
    print("4. Exit")

    choice = input("Please select an option: ")

    if choice == '1':
        enter_income()
    elif choice == '2':
        enter_debt()
    elif choice == '3':
        check_dti_ratio()
    elif choice == '4':
        print("Exiting the program. Goodbye!")
    else:
        print("Invalid choice. Please try again.")
        main_menu()

def enter_income():
    hold_percent = 0
    tax_percent = 0
    net_income = 0
    main_menu()

def enter_debt():
    debt_collection = []
    user_command = input(f'Enter debt amount or “finish” to finish or “undo” to remove last input: ').lower
    debt = input("Please enter your debt: ")
    main_menu()

def check_dti_ratio():
    main_menu()