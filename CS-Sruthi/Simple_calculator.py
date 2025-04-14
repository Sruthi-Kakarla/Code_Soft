def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero is not allowed."
    return x / y

def calculator():
    print("\n===== Simple Calculator =====")
    print("Operations:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    
    while True:
        # Get operation choice
        choice = input("\nEnter choice (1/2/3/4): ")
        
        # Validate operation choice
        if choice in ('1', '2', '3', '4'):
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
                
            if choice == '1':
                result = add(num1, num2)
                operation = '+'
            elif choice == '2':
                result = subtract(num1, num2)
                operation = '-'
            elif choice == '3':
                result = multiply(num1, num2)
                operation = '*'
            elif choice == '4':
                result = divide(num1, num2)
                operation = '/'
                
            # Check if result is an error message
            if isinstance(result, str):
                print(result)
            else:
                print(f"\n{num1} {operation} {num2} = {result}")
                
            # Ask user if they want to perform another calculation
            another_calculation = input("\nDo you want to perform another calculation? (yes/no): ")
            if another_calculation.lower() != 'yes':
                print("Thank you for using the calculator. Goodbye!")
                break
        else:
            print("Invalid input. Please enter a valid choice (1/2/3/4).")

if __name__ == "__main__":
    calculator()