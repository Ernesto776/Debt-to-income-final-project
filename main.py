def main_menu():
    print("Welcome to the Main Menu")
    print("1. Enter Income")
    print("2. Enter Debt")
    print("3. Exit")

    choice = input("Please select an option: ")

    if choice == '1':
        enter_income()
    elif choice == '2':
        enter_debt()
    elif choice == '3':
        print("Exiting the program. Goodbye!")
    else:
        print("Invalid choice. Please try again.")
        main_menu()