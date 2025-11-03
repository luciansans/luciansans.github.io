import tkinter as tk
from tkinter import messagebox

def show_info():
    name_label.config(text=" Lucian Blake")
    address_label.config(text=" 123 Main St, Cape town, South-Africa")

def quit_program():
    root.quit()

# Create  window
root = tk.Tk()
root.title("Name and Address Display")

# Create labels to display name and address
name_label = tk.Label(root, text="", font=("Arial", 14))
address_label = tk.Label(root, text="", font=("Arial", 14))

name_label.pack(pady=10)
address_label.pack(pady=10)

# Create buttons 
show_info_button = tk.Button(root, text="Show Info", command=show_info, font=("Arial", 14))
quit_button = tk.Button(root, text="Quit Program", command=quit_program, font=("Arial", 14))

show_info_button.pack(pady=10)
quit_button.pack(pady=10)

# Start the GUI  loop
root.mainloop()
