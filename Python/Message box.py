import tkinter as tk
from tkinter import messagebox

def calculate_average():
    try:
        # Get test scores from Entry widgets
        test1 = float(test1_entry.get())
        test2 = float(test2_entry.get())
        test3 = float(test3_entry.get())

        # Calculate the average
        average = (test1 + test2 + test3) / 3

        # Display the average under the input fields
        average_label.config(text=f"Average: {average:.2f}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric test scores.")

def quit_program():
    root.quit()

# Create the main window
root = tk.Tk()
root.title("Test Score Average Calculator")

# Create labels
label1 = tk.Label(root, text="Enter the score for test 1:")
label2 = tk.Label(root, text="Enter the score for test 2:")
label3 = tk.Label(root, text="Enter the score for test 3:")

# Create Entry widgets
test1_entry = tk.Entry(root)
test2_entry = tk.Entry(root)
test3_entry = tk.Entry(root)

# Create a label to display the average
average_label = tk.Label(root, text="", font=("Arial", 14))

# Create buttons
calculate_button = tk.Button(root, text="Average", command=calculate_average)
quit_button = tk.Button(root, text="Quit", command=quit_program)


# Layout labels, Entry widgets, buttons, and average label
label1.grid(row=0, column=0, padx=10, pady=5)
label2.grid(row=1, column=0, padx=10, pady=5)
label3.grid(row=2, column=0, padx=10, pady=5)

test1_entry.grid(row=0, column=1, padx=10, pady=5)
test2_entry.grid(row=1, column=1, padx=10, pady=5)
test3_entry.grid(row=2, column=1, padx=10, pady=5)

calculate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
quit_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

average_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Start the GUI main loop
root.mainloop()
