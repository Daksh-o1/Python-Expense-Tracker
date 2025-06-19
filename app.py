import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import csv
from datetime import datetime
import os
import uuid
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# --- Configuration ---
EXPENSE_FILE = 'expenses.csv'
HEADERS = ['ID', 'Date', 'Description', 'Amount']

# --- CSV File Handling Functions (No Change) ---
def initialize_csv():
    if not os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)
        print(f"Created new expense file: {EXPENSE_FILE}")
    else:
        with open(EXPENSE_FILE, 'r', newline='') as file:
            reader = csv.reader(file)
            first_row = next(reader, None)
            if first_row != HEADERS:
                messagebox.showwarning("CSV Warning", "Your CSV file headers might be outdated or missing 'ID' column. Please consider starting with a fresh CSV.")

def add_expense_to_csv(date, description, amount):
    try:
        amount_float = float(amount)
        if amount_float <= 0:
            return False, "Amount must be positive."
        datetime.strptime(date, '%Y-%m-%d')
        expense_id = str(uuid.uuid4())
        with open(EXPENSE_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([expense_id, date, description, amount_float])
        return True, "Expense added successfully!"
    except ValueError:
        return False, "Invalid amount or date format. Please use YYYY-MM-DD for date and a number for amount."
    except Exception as e:
        return False, f"An error occurred: {e}"

def get_all_expenses():
    expenses = []
    try:
        with open(EXPENSE_FILE, 'r', newline='') as file:
            reader = csv.DictReader(file)
            if reader.fieldnames != HEADERS:
                messagebox.showwarning("CSV Error", f"CSV file headers are incorrect. Expected {HEADERS}, found {reader.fieldnames}. Please fix the CSV or delete it to regenerate.")
                return []
            for row in reader:
                expenses.append(row)
    except FileNotFoundError:
        pass
    except Exception as e:
        messagebox.showerror("File Error", f"Could not read expenses from CSV: {e}")
    return expenses

def update_expense_in_csv(expense_id, new_date, new_description, new_amount):
    all_expenses = get_all_expenses()
    updated_expenses = []
    found = False
    for expense in all_expenses:
        if expense.get('ID') == expense_id:
            try:
                amount_float = float(new_amount)
                datetime.strptime(new_date, '%Y-%m-%d')
                updated_expenses.append({'ID': expense_id, 'Date': new_date, 'Description': new_description, 'Amount': amount_float})
                found = True
            except ValueError:
                return False, "Invalid amount or date format for update."
        else:
            updated_expenses.append(expense)
    if not found:
        return False, "Expense not found for update."
    try:
        with open(EXPENSE_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(updated_expenses)
        return True, "Expense updated successfully!"
    except Exception as e:
        return False, f"Error updating expense: {e}"

def delete_expense_from_csv(expense_id):
    all_expenses = get_all_expenses()
    updated_expenses = [exp for exp in all_expenses if exp.get('ID') != expense_id]
    if len(updated_expenses) == len(all_expenses):
        return False, "Expense not found for deletion."
    try:
        with open(EXPENSE_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(updated_expenses)
        return True, "Expense deleted successfully!"
    except Exception as e:
        return False, f"Error deleting expense: {e}"

def get_monthly_summary(year, month):
    total_monthly_expense = 0
    all_expenses = get_all_expenses()
    for expense in all_expenses:
        try:
            expense_date = datetime.strptime(expense['Date'], '%Y-%m-%d')
            if expense_date.year == int(year) and expense_date.month == int(month):
                total_monthly_expense += float(expense['Amount'])
        except (ValueError, KeyError):
            continue
    return total_monthly_expense

def get_monthly_totals_for_graph():
    monthly_totals = {}
    all_expenses = get_all_expenses()
    for expense in all_expenses:
        try:
            expense_date = datetime.strptime(expense['Date'], '%Y-%m-%d')
            month_key = expense_date.strftime('%Y-%m')
            amount = float(expense['Amount'])
            monthly_totals[month_key] = monthly_totals.get(month_key, 0) + amount
        except (ValueError, KeyError):
            continue
    return dict(sorted(monthly_totals.items()))

# --- Tkinter GUI Application ---
class ExpenseTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("Modern Expense Tracker")
        master.geometry("1000x750") # Slightly taller
        master.minsize(850, 650)

        ### Enhanced Styling ###
        self.style = ttk.Style()
        self.style.theme_use('clam') # A clean, modern theme
        self.base_font = ('Segoe UI', 10)
        self.heading_font = ('Segoe UI', 11, 'bold')
        self.title_font = ('Segoe UI', 16, 'bold')
        self.emphasis_font = ('Segoe UI', 10, 'italic')

        self.style.configure("TLabel", font=self.base_font)
        self.style.configure("TButton", font=('Segoe UI', 10, 'bold'), padding=8)
        self.style.configure("TEntry", font=self.base_font)
        self.style.configure("Treeview.Heading", font=('Segoe UI', 11, 'bold'))
        self.style.configure("Treeview", font=self.base_font)
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'), padding=(10, 5))

        ### Color Palette ###
        self.primary_color = '#4CAF50'   # Green
        self.secondary_color = '#3F51B5' # Indigo
        self.accent_color = '#FF9800'    # Orange
        self.bg_color = '#f0f0f0'        # Light Gray
        self.text_color = '#333333'      # Dark Gray
        self.error_color = '#f44336'     # Red
        self.success_color = '#43A047'   # Dark Green

        master.config(bg=self.bg_color)

        # --- Notebook (Tabs) ---
        self.notebook = ttk.Notebook(master, style='TNotebook')
        self.notebook.pack(expand=True, fill='both', padx=15, pady=15)

        self.add_expense_tab = ttk.Frame(self.notebook, style='TFrame')
        self.view_expenses_tab = ttk.Frame(self.notebook, style='TFrame')
        self.reports_tab = ttk.Frame(self.notebook, style='TFrame')

        self.notebook.add(self.add_expense_tab, text='Add Expense')
        self.notebook.add(self.view_expenses_tab, text='View/Manage')
        self.notebook.add(self.reports_tab, text='Analytics & Export')

        ### Configure tab frame background
        self.style.configure('TFrame', background=self.bg_color)

        # --- Initialize Tabs ---
        self._setup_add_expense_tab()
        self._setup_view_expenses_tab()
        self._setup_reports_tab()

        self.load_expenses()
        self.update_summary_display()

    def _setup_add_expense_tab(self):
        self.add_expense_tab.columnconfigure(1, weight=1)
        for i in range(4):
            self.add_expense_tab.rowconfigure(i, weight=1)

        ### Styled Labels and Entry Fields ###
        ttk.Label(self.add_expense_tab, text="Date (YYYY-MM-DD):", font=self.heading_font).grid(row=0, column=0, sticky='w', padx=10, pady=8)
        self.date_entry = ttk.Entry(self.add_expense_tab, width=40, font=self.base_font)
        self.date_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=8)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))

        ttk.Label(self.add_expense_tab, text="Description:", font=self.heading_font).grid(row=1, column=0, sticky='w', padx=10, pady=8)
        self.description_entry = ttk.Entry(self.add_expense_tab, width=40, font=self.base_font)
        self.description_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=8)

        ttk.Label(self.add_expense_tab, text="Amount:", font=self.heading_font).grid(row=2, column=0, sticky='w', padx=10, pady=8)
        self.amount_entry = ttk.Entry(self.add_expense_tab, width=40, font=self.base_font)
        self.amount_entry.grid(row=2, column=1, sticky='ew', padx=10, pady=8)

        ### Primary Color for Add Button ###
        self.add_button = ttk.Button(self.add_expense_tab, text="Add Expense", command=self.add_expense, style='Primary.TButton')
        self.style.configure('Primary.TButton', foreground='white', background=self.primary_color)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=20)

    def _setup_view_expenses_tab(self):
        tree_frame = tk.Frame(self.view_expenses_tab, bg=self.bg_color)
        tree_frame.pack(side='top', fill='both', expand=True, padx=15, pady=10)

        display_headers = [h for h in HEADERS if h != 'ID']
        self.tree = ttk.Treeview(tree_frame, columns=display_headers, show='headings')

        for col in display_headers:
            self.tree.heading(col, text=col)
            if col == 'Date':
                self.tree.column(col, width=120, anchor='center')
            elif col == 'Amount':
                self.tree.column(col, width=100, anchor='e')
            else:
                self.tree.column(col, width=250, anchor='w')

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        button_frame = tk.Frame(self.view_expenses_tab, bg=self.bg_color, pady=10)
        button_frame.pack(side='top', fill='x', padx=15)

        ### Use themed buttons with a consistent style
        self.edit_button = ttk.Button(button_frame, text="Edit Selected", command=self.edit_expense)
        self.edit_button.pack(side='left', padx=5, pady=8)

        self.delete_button = ttk.Button(button_frame, text="Delete Selected", command=self.delete_expense)
        self.delete_button.pack(side='left', padx=5, pady=8)

        summary_frame = tk.Frame(self.view_expenses_tab, bg=self.bg_color, bd=2, relief='groove', padx=15, pady=15)
        summary_frame.pack(pady=15, fill='x', padx=15)
        summary_frame.columnconfigure(1, weight=1)

        ttk.Label(summary_frame, text="Monthly Summary:", font=self.title_font).grid(row=0, column=0, sticky='w', pady=8)
        self.summary_label = ttk.Label(summary_frame, text="Total for this month: ₹0.00", font=('Segoe UI', 14, 'bold'), foreground=self.secondary_color)
        self.summary_label.grid(row=0, column=1, sticky='ew', pady=8)

        current_year = datetime.now().year
        current_month = datetime.now().month

        ttk.Label(summary_frame, text="Year:", font=self.heading_font).grid(row=1, column=0, sticky='w', pady=5)
        self.summary_year_var = tk.StringVar(self.master)
        self.summary_year_var.set(str(current_year))
        self.summary_year_dropdown = ttk.OptionMenu(summary_frame, self.summary_year_var, str(current_year),
                                                    *map(str, range(current_year - 5, current_year + 2)))
        self.summary_year_dropdown.grid(row=1, column=1, sticky='w', pady=5)
        self.summary_year_var.trace_add('write', self.update_summary_display)

        ttk.Label(summary_frame, text="Month:", font=self.heading_font).grid(row=2, column=0, sticky='w', pady=5)
        self.summary_month_var = tk.StringVar(self.master)
        self.summary_month_var.set(str(current_month))
        self.summary_month_dropdown = ttk.OptionMenu(summary_frame, self.summary_month_var, str(current_month),
                                                     *map(str, range(1, 13)))
        self.summary_month_dropdown.grid(row=2, column=1, sticky='w', pady=5)
        self.summary_month_var.trace_add('write', self.update_summary_display)

    def _setup_reports_tab(self):
        ### Consistent background color
        reports_frame = tk.Frame(self.reports_tab, bg=self.bg_color, padx=15, pady=15)
        reports_frame.pack(fill='both', expand=True)

        ### Use grid for better layout in Reports tab
        reports_frame.columnconfigure(0, weight=1)
        reports_frame.rowconfigure(0, weight=0) # Export area
        reports_frame.rowconfigure(1, weight=1) # Graph area

        ### Export to Excel Section
        export_frame = tk.Frame(reports_frame, bd=2, relief='groove', padx=10, pady=10, bg=self.bg_color)
        export_frame.grid(row=0, column=0, sticky='ew', pady=10, padx=10)
        ttk.Label(export_frame, text="Export Data", font=self.title_font, foreground=self.secondary_color).pack(pady=5)
        export_button = ttk.Button(export_frame, text="Export All to Excel", command=self.export_to_excel)
        export_button.pack(pady=8)

        ### Graph View Section
        graph_container = tk.Frame(reports_frame, bd=2, relief='groove', padx=10, pady=10, bg='white') # White background for the graph area
        graph_container.grid(row=1, column=0, sticky='nsew', pady=10, padx=10)
        ttk.Label(graph_container, text="Monthly Expense Trend", font=self.title_font, foreground=self.secondary_color).pack(pady=5)

        self.fig, self.ax = plt.subplots(figsize=(8, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_container)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, graph_container)
        toolbar.update()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.draw_monthly_graph()
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)

    def add_expense(self):
        date = self.date_entry.get()
        description = self.description_entry.get()
        amount = self.amount_entry.get()

        if not date or not description or not amount:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        success, msg = add_expense_to_csv(date, description, amount)
        if success:
            messagebox.showinfo("Success", msg, icon='info') ### Added icon
            self.clear_add_entries()
            self.load_expenses()
            self.update_summary_display()
            self.draw_monthly_graph()
            self.notebook.select(self.view_expenses_tab)
        else:
            messagebox.showerror("Error", msg, icon='error') ### Added icon

    def clear_add_entries(self):
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

    def load_expenses(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        expenses = get_all_expenses()
        for expense in expenses:
            display_values = [expense.get(h, '') for h in HEADERS if h != 'ID']
            self.tree.insert('', tk.END, iid=expense.get('ID'), values=display_values)

    def update_summary_display(self, *args):
        try:
            year = int(self.summary_year_var.get())
            month = int(self.summary_month_var.get())
            total = get_monthly_summary(year, month)
            self.summary_label.config(text=f"Total for {datetime(year, month, 1).strftime('%B %Y')}: ₹{total:.2f}")
        except ValueError:
            self.summary_label.config(text="Invalid selection")
        except Exception as e:
            self.summary_label.config(text=f"Error: {e}")

    def edit_expense(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an expense to edit.")
            return

        expense_id_to_edit = selected_item
        expenses = get_all_expenses()
        selected_expense_data = None
        for exp in expenses:
            if exp.get('ID') == expense_id_to_edit:
                selected_expense_data = exp
                break

        if not selected_expense_data:
            messagebox.showerror("Error", "Selected expense data not found.")
            return

        edit_window = tk.Toplevel(self.master)
        edit_window.title("Edit Expense")
        edit_window.geometry("400x280") # Slightly taller edit window
        edit_window.transient(self.master)
        edit_window.grab_set()

        ttk.Label(edit_window, text="Date (YYYY-MM-DD):", font=self.heading_font).grid(row=0, column=0, padx=10, pady=8, sticky='w')
        edit_date_entry = ttk.Entry(edit_window, width=30, font=self.base_font)
        edit_date_entry.grid(row=0, column=1, padx=10, pady=8, sticky='ew')
        edit_date_entry.insert(0, selected_expense_data.get('Date', ''))

        ttk.Label(edit_window, text="Description:", font=self.heading_font).grid(row=1, column=0, padx=10, pady=8, sticky='w')
        edit_description_entry = ttk.Entry(edit_window, width=30, font=self.base_font)
        edit_description_entry.grid(row=1, column=1, padx=10, pady=8, sticky='ew')
        edit_description_entry.insert(0, selected_expense_data.get('Description', ''))

        ttk.Label(edit_window, text="Amount:", font=self.heading_font).grid(row=2, column=0, padx=10, pady=8, sticky='w')
        edit_amount_entry = ttk.Entry(edit_window, width=30, font=self.base_font)
        edit_amount_entry.grid(row=2, column=1, padx=10, pady=8, sticky='ew')
        edit_amount_entry.insert(0, selected_expense_data.get('Amount', ''))

        def save_changes():
            new_date = edit_date_entry.get()
            new_description = edit_description_entry.get()
            new_amount = edit_amount_entry.get()
            success, msg = update_expense_in_csv(expense_id_to_edit, new_date, new_description, new_amount)
            if success:
                messagebox.showinfo("Success", msg, icon='info')
                self.load_expenses()
                self.update_summary_display()
                self.draw_monthly_graph()
                edit_window.destroy()
            else:
                messagebox.showerror("Error", msg, icon='error')

        save_button = ttk.Button(edit_window, text="Save Changes", command=save_changes, style='Primary.TButton')
        save_button.grid(row=3, column=0, columnspan=2, pady=15)

    def delete_expense(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an expense to delete.")
            return

        expense_id_to_delete = selected_item
        item_values = self.tree.item(selected_item, 'values')
        confirmation_text = f"Are you sure you want to delete:\nDate: {item_values}?" # Improved display

        confirm = messagebox.askyesno("Confirm Deletion", confirmation_text)
        if confirm:
            success, msg = delete_expense_from_csv(expense_id_to_delete)
            if success:
                messagebox.showinfo("Success", msg, icon='info')
                self.load_expenses()
                self.update_summary_display()
                self.draw_monthly_graph()
            else:
                messagebox.showerror("Error", msg, icon='error')

    def export_to_excel(self):
        expenses = get_all_expenses()
        if not expenses:
            messagebox.showwarning("No Data", "No expenses to export.")
            return
        try:
            df = pd.DataFrame(expenses)
            df_display = df[[col for col in HEADERS if col != 'ID']]
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Save Expenses as Excel"
            )
            if file_path:
                df_display.to_excel(file_path, index=False)
                messagebox.showinfo("Export Success", f"Expenses exported to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export to Excel: {e}")

    def draw_monthly_graph(self):
        monthly_data = get_monthly_totals_for_graph()
        months = list(monthly_data.keys())
        totals = list(monthly_data.values())

        self.ax.clear()

        if not months:
            self.ax.text(0.5, 0.5, "No data to display graph", ha='center', va='center', transform=self.ax.transAxes, fontsize=12)
            self.canvas.draw_idle()
            return

        self.ax.bar(months, totals, color=self.primary_color)
        self.ax.set_xlabel("Month", fontsize=10)
        self.ax.set_ylabel("Total Amount (₹)", fontsize=10)
        self.ax.set_title("Monthly Expense Overview", fontsize=12, fontweight='bold', color=self.secondary_color)
        self.ax.tick_params(axis='x', rotation=45, labelsize=9)
        self.ax.tick_params(axis='y', labelsize=9)
        self.fig.tight_layout()
        self.canvas.draw_idle()

    def _on_tab_change(self, event):
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        if selected_tab == "Analytics & Export":
            self.draw_monthly_graph()

# --- Main Application Entry Point ---
if __name__ == "__main__":
    initialize_csv()
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()