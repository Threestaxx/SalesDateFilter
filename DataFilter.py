import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox

# Load the dataset
def load_data():
    try:
        df = pd.read_csv('Sample - Superstore.csv', encoding='latin1')
        print("Dataset loaded successfully!")
        return df
    except FileNotFoundError:
        messagebox.showerror("Error", "File 'Sample - Superstore.csv' not found. Please ensure the file is in the correct directory.")
        exit()
    except UnicodeDecodeError:
        messagebox.showerror("Error", "Unable to read the file. Please check the file encoding.")
        exit()

# Filter data based on user input
def filter_data(df, filter_type, value):
    if filter_type == "Region":
        return df[df['Region'] == value]
    elif filter_type == "Category":
        return df[df['Category'] == value]
    elif filter_type == "Sales Range":
        min_sales, max_sales = map(float, value.split(','))
        return df[(df['Sales'] >= min_sales) & (df['Sales'] <= max_sales)]
    elif filter_type == "Profit Range":
        min_profit, max_profit = map(float, value.split(','))
        return df[(df['Profit'] >= min_profit) & (df['Profit'] <= max_profit)]
    elif filter_type == "State":
        return df[df['State'] == value]
    else:
        return None

# Function to handle the "Filter" button click
def on_filter():
    filter_type = filter_var.get()
    value = entry.get().strip()

    if filter_type in ["Sales Range", "Profit Range"]:
        min_value = min_entry.get().strip()
        max_value = max_entry.get().strip()
        if not min_value or not max_value:
            messagebox.showwarning("Input Error", "Please enter both min and max values.")
            return
        try:
            min_value = float(min_value)
            max_value = float(max_value)
            value = f"{min_value},{max_value}"
        except ValueError:
            messagebox.showwarning("Input Error", "Min and max values must be numbers.")
            return
    elif not value:
        messagebox.showwarning("Input Error", "Please enter a value to filter.")
        return

    try:
        filtered_data = filter_data(df, filter_type, value)
        if filtered_data is not None and not filtered_data.empty:
            result_text.delete(1.0, tk.END)  # Clear previous results
            result_text.insert(tk.END, filtered_data.to_string())
        else:
            messagebox.showinfo("No Results", "No data found matching your criteria.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to update the UI based on the selected filter type
def update_ui(event=None):
    filter_type = filter_var.get()
    if filter_type in ["Sales Range", "Profit Range"]:
        min_label.grid(row=2, column=0, padx=10, pady=10)
        min_entry.grid(row=2, column=1, padx=10, pady=10)
        max_label.grid(row=3, column=0, padx=10, pady=10)
        max_entry.grid(row=3, column=1, padx=10, pady=10)
        entry_label.grid_remove()
        entry.grid_remove()
    else:
        min_label.grid_remove()
        min_entry.grid_remove()
        max_label.grid_remove()
        max_entry.grid_remove()
        entry_label.grid(row=1, column=0, padx=10, pady=10)
        entry.grid(row=1, column=1, padx=10, pady=10)

# Main application window
app = tk.Tk()
app.title("Superstore Data Filter")
app.geometry("800x600")

# Load the dataset
df = load_data()

# Dropdown for filter type
filter_var = tk.StringVar()
filter_label = ttk.Label(app, text="Filter By:")
filter_label.grid(row=0, column=0, padx=10, pady=10)
filter_dropdown = ttk.Combobox(app, textvariable=filter_var, values=["Region", "Category", "Sales Range", "Profit Range", "State"])
filter_dropdown.grid(row=0, column=1, padx=10, pady=10)
filter_dropdown.current(0)  # Set default selection
filter_dropdown.bind("<<ComboboxSelected>>", update_ui)  # Update UI when selection changes

# Entry for filter value
entry_label = ttk.Label(app, text="Enter Value:")
entry_label.grid(row=1, column=0, padx=10, pady=10)
entry = ttk.Entry(app, width=50)
entry.grid(row=1, column=1, padx=10, pady=10)

# Min and Max entries (initially hidden)
min_label = ttk.Label(app, text="Min Value:")
min_entry = ttk.Entry(app, width=20)
max_label = ttk.Label(app, text="Max Value:")
max_entry = ttk.Entry(app, width=20)

# Filter button
filter_button = ttk.Button(app, text="Filter", command=on_filter)
filter_button.grid(row=4, column=0, columnspan=2, pady=10)

# Function to clear all inputs and results
def clear_inputs():
    # Reset filter dropdown
    filter_dropdown.current(0)
    update_ui()  # Update the UI to show/hide min/max fields

    # Clear entry fields
    entry.delete(0, tk.END)
    min_entry.delete(0, tk.END)
    max_entry.delete(0, tk.END)

    # Clear results text area
    result_text.delete(1.0, tk.END)

# Add the Clear Button next to the Filter Button
clear_button = ttk.Button(app, text="Clear", command=clear_inputs)
clear_button.grid(row=4, column=1, padx=10, pady=10)  # Place it next to the Filter Button

# Text widget to display results
result_text = tk.Text(app, wrap=tk.NONE, width=100, height=20)
result_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Scrollbars for the text widget
scroll_y = ttk.Scrollbar(app, orient=tk.VERTICAL, command=result_text.yview)
scroll_y.grid(row=5, column=2, sticky=tk.NS)
result_text.config(yscrollcommand=scroll_y.set)

scroll_x = ttk.Scrollbar(app, orient=tk.HORIZONTAL, command=result_text.xview)
scroll_x.grid(row=6, column=0, columnspan=2, sticky=tk.EW)
result_text.config(xscrollcommand=scroll_x.set)

# Run the application
app.mainloop()