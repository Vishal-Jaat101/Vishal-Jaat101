def add(x, y):
    """Add two numbers"""
    return x + y


def subtract(x, y):
    """Subtract two numbers"""
    return x - y


def multiply(x, y):
    """Multiply two numbers"""
    return x * y


def divide(x, y):
    """Divide two numbers"""
    if y == 0:
        return "Error! Division by zero."
    return x / y


def calculator():
    """Main calculator function"""
    print("Simple Calculator")
    print("-" * 40)
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Jadu dekhna hai kya")
    print("6. Choose 0")
    print("7. Kuch to galat h idhar")
    print("8. Arey 0 se divide karke dekh ek baar")
    print("9. Google pe search karna")
    print("0. Bahar jao bhaiya")
    print("-" * 40)

    while True:
        choice = input("\nEnter choice (1/2/3/4/5/6/7/8/9/0): ")

        if choice == "0":
            print("Bhai khud hi bahar jao, main toh yahan hi rahunga! 😂")
            break

        if choice in ("1", "2", "3", "4", "5", "6", "7", "8", "9"):
            try:
                if choice == "8":
                    num1 = float(input("Enter first number: "))
                    print(f"{num1} ÷ 0 = {divide(num1, 0)} \nBhai jab 0 se divide karega to tera wo crush ke sath relationship ka result aayega!😂")
                elif choice == "5":
                    print("Calculator ka use karne aaya tha whi kar jyada jadu mat dekh usne kam jadu kiya tha tere par jo ek or jadu dekhna h terko")
                elif choice == "6":
                    print("Sorry for the inconvenience the number choosed by you is not in my range because developer was just playing with the code and don't you see gadhe its saying to choose 0 itna bhi nahi aata hai kya bhen ke bhaiya")
                elif choice == "7":
                    print("Sab shi h bas aapka dimaag kharab hai")
                elif choice == "9":
                    print("Calculator h ye isme numbers ka use hota h na ki google ka")
                else:
                    num1 = float(input("Enter first number: "))
                    num2 = float(input("Enter second number: "))

                    if choice == "1":
                        print(f"{num1} + {num2} = {add(num1, num2)}")
                    elif choice == "2":
                        print(f"{num1} - {num2} = {subtract(num1, num2)}")
                    elif choice == "3":
                        print(f"{num1} × {num2} = {multiply(num1, num2)}")
                    elif choice == "4":
                        result = divide(num1, num2)
                        print(f"{num1} ÷ {num2} = {result}")
            except ValueError:
                print("Kya Gawar h bhai tu number daalna bhi nhi aata chiichii! Kripya ek valid number enter kare anytha ye kaam nhi karega aapke dimag ki trha.")
        else:
            print("1 se 9 or 0 dikh rha h shayad nhi jra doctor ke paas jao aur apne aankh dikhao")


if __name__ == "__main__":
    calculator()
