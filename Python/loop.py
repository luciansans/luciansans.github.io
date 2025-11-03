def concatenate_strings():
    string1 = input("Enter the first string: ")
    string2 = input("Enter the second string: ")
    result = string1 + string2
    print("Concatenate strings:", result)

def convert_to_uppercase():
    string = input("Enter a string: ")
    result = string.upper()
    print("Uppercase string:", result)

def convert_to_lowercase():
    string = input("Enter a string: ")
    result = string.lower()
    print("Lowercase string:", result)

# Display the menu options
def display_menu():
    print(" String Operations Menu:")
    print("1. Concatenate with two strings")
    print("2. Convert a string to uppercase")
    print("3. Convert a string to lowercase")
    print("4. Exit")

# Perform selected operation based on user input
def perform_operation(choice):
    if choice == "1":
        concatenate_strings()
    elif choice == "2":
        convert_to_uppercase()
    elif choice == "3":
        convert_to_lowercase()
    elif choice == "4":
        print("Exiting the program...")
        exit()
    else:
        print("Invalid choice! Please select a valid menu option.")

# Main program loop
while True:
    display_menu()
    user_choice = input("Enter your choice (1-4): ")
    if user_choice in ["1", "2", "3", "4"]:
        perform_operation(user_choice)
    else:
        print("Invalid choice! Please enter a valid menu option.")