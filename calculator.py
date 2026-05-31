import tkinter as tk
from tkinter import ttk


def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y


def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    return x / y


def get_number(entry):
    value = entry.get().strip()
    if not value:
        raise ValueError("Enter a number")
    return float(value)


def show_result(label, message):
    label.config(text=message)


def handle_operation(operation, num1_entry, num2_entry, result_label):
    try:
        num1 = get_number(num1_entry)
        num2 = get_number(num2_entry)
    except ValueError as exc:
        show_result(result_label, f"Error: {exc}")
        return

    if operation == "add":
        show_result(result_label, f"{num1} + {num2} = {add(num1, num2)}")
    elif operation == "subtract":
        show_result(result_label, f"{num1} - {num2} = {subtract(num1, num2)}")
    elif operation == "multiply":
        show_result(result_label, f"{num1} × {num2} = {multiply(num1, num2)}")
    elif operation == "divide":
        result = divide(num1, num2)
        show_result(result_label, f"{num1} ÷ {num2} = {result}")


def handle_choice_8(num1_entry, result_label):
    try:
        num1 = get_number(num1_entry)
    except ValueError as exc:
        show_result(result_label, f"Error: {exc}")
        return

    result = divide(num1, 0)
    show_result(
        result_label,
        f"{num1} ÷ 0 = {result}\nBhai jab 0 se divide karega to tera wo crush ke sath relationship ka result aayega! 😂",
    )


def handle_magic(result_label):
    show_result(
        result_label,
        "Calculator ka use karne aaya tha whi kar, jyada jadu mat dekh.",
    )


def handle_choose_0(result_label):
    show_result(
        result_label,
        "Sorry, the number choosed by you is not in my range because developer was busy playing.",
    )


def handle_wrong(result_label):
    show_result(result_label, "Sab shi h bas aapka dimaag kharab hai")


def handle_google(result_label):
    show_result(result_label, "Calculator h ye, isme numbers ka use hota h na ki Google ka")


def clear_inputs(num1_entry, num2_entry, result_label):
    num1_entry.delete(0, tk.END)
    num2_entry.delete(0, tk.END)
    show_result(result_label, "Result will appear here.")


def bind_shortcuts(root, num1_entry, num2_entry, result_label):
    root.bind("<Return>", lambda event: handle_operation("add", num1_entry, num2_entry, result_label))
    root.bind("+", lambda event: handle_operation("add", num1_entry, num2_entry, result_label))
    root.bind("-", lambda event: handle_operation("subtract", num1_entry, num2_entry, result_label))
    root.bind("*", lambda event: handle_operation("multiply", num1_entry, num2_entry, result_label))
    root.bind("/", lambda event: handle_operation("divide", num1_entry, num2_entry, result_label))
    root.bind("8", lambda event: handle_choice_8(num1_entry, result_label))
    root.bind("m", lambda event: handle_magic(result_label))
    root.bind("0", lambda event: handle_choose_0(result_label))
    root.bind("g", lambda event: handle_google(result_label))


def create_ui():
    root = tk.Tk()
    root.title("Simple Calculator")
    root.resizable(True, True)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    style = ttk.Style(root)
    style.configure("TButton", padding=6)
    style.configure("TLabel", padding=4)

    frame = ttk.Frame(root, padding=20)
    frame.grid(row=0, column=0, sticky="NSEW")

    ttk.Label(frame, text="Simple Calculator", font=(None, 18, "bold")).grid(
        row=0, column=0, columnspan=3, pady=(0, 16)
    )

    ttk.Label(frame, text="First number:").grid(row=1, column=0, sticky="W")
    num1_entry = ttk.Entry(frame, width=24)
    num1_entry.grid(row=1, column=1, columnspan=2, sticky="WE", pady=4)

    ttk.Label(frame, text="Second number:").grid(row=2, column=0, sticky="W")
    num2_entry = ttk.Entry(frame, width=24)
    num2_entry.grid(row=2, column=1, columnspan=2, sticky="WE", pady=4)

    result_label = ttk.Label(
        frame,
        text="Result will appear here.",
        foreground="blue",
        wraplength=360,
        justify="center",
    )
    result_label.grid(row=3, column=0, columnspan=3, pady=(12, 12))

    ttk.Label(
        frame,
        text="Shortcuts: Enter=Add, + - * /, 8=ZeroDiv, m=Magic, 0=Choose0, g=Google",
        foreground="gray",
        wraplength=360,
        justify="center",
    ).grid(row=4, column=0, columnspan=3, pady=(0, 12))

    ttk.Button(
        frame,
        text="Add",
        command=lambda: handle_operation("add", num1_entry, num2_entry, result_label),
        width=14,
    ).grid(row=5, column=0, padx=4, pady=4)

    ttk.Button(
        frame,
        text="Subtract",
        command=lambda: handle_operation("subtract", num1_entry, num2_entry, result_label),
        width=14,
    ).grid(row=5, column=1, padx=4, pady=4)

    ttk.Button(
        frame,
        text="Multiply",
        command=lambda: handle_operation("multiply", num1_entry, num2_entry, result_label),
        width=14,
    ).grid(row=5, column=2, padx=4, pady=4)

    ttk.Button(
        frame,
        text="Divide",
        command=lambda: handle_operation("divide", num1_entry, num2_entry, result_label),
        width=14,
    ).grid(row=6, column=0, padx=4, pady=4)

    ttk.Button(
        frame,
        text="Zero se Divide kare to?",
        command=lambda: handle_choice_8(num1_entry, result_label),
        width=26,
    ).grid(row=6, column=1, padx=4, pady=4)

    ttk.Button(
        frame,
        text="Clear",
        command=lambda: clear_inputs(num1_entry, num2_entry, result_label),
        width=14,
    ).grid(row=6, column=2, padx=4, pady=4)

    ttk.Button(
        frame,
        text="JADU DEKH",
        command=lambda: handle_magic(result_label),
        width=14,
    ).grid(row=7, column=0, padx=4, pady=4)

    ttk.Button(
        frame,
        text="Choose 0",
        command=lambda: handle_choose_0(result_label),
        width=14,
    ).grid(row=7, column=1, padx=4, pady=4)

    ttk.Button(
        frame,
        text="Google",
        command=lambda: handle_google(result_label),
        width=14,
    ).grid(row=7, column=2, padx=4, pady=4)

    bind_shortcuts(root, num1_entry, num2_entry, result_label)

    num1_entry.focus()
    root.mainloop()


if __name__ == "__main__":
    create_ui()
