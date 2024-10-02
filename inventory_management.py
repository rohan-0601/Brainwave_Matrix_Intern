import tkinter as tk
from tkinter import messagebox
import sqlite3


class InventoryManagementSystem:
    def __init__(self, root):  # Fixed constructor
        self.root = root
        self.root.title("Inventory Management System")
        self.conn = sqlite3.connect('inventory.db')
        self.create_tables()
        self.create_widgets()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT
                )''')

            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS inventory (
                    id INTEGER PRIMARY KEY,
                    product_name TEXT UNIQUE,
                    quantity INTEGER,
                    price REAL
                )''')

    def create_widgets(self):
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2)

        self.signup_button = tk.Button(self.login_frame, text="Sign Up", command=self.signup)
        self.signup_button.grid(row=3, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            self.login_frame.pack_forget()
            self.show_inventory_management()
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            try:
                with self.conn:
                    self.conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                messagebox.showinfo("Success", "User created successfully. You can now log in.")
            except sqlite3.IntegrityError:
                messagebox.showerror("Signup Error", "Username already exists.")
        else:
            messagebox.showerror("Signup Error", "Please enter a username and password.")

    def show_inventory_management(self):
        self.inventory_frame = tk.Frame(self.root)
        self.inventory_frame.pack(pady=20)

        self.product_name_label = tk.Label(self.inventory_frame, text="Product Name:")
        self.product_name_label.grid(row=0, column=0)
        self.product_name_entry = tk.Entry(self.inventory_frame)
        self.product_name_entry.grid(row=0, column=1)

        self.quantity_label = tk.Label(self.inventory_frame, text="Quantity:")
        self.quantity_label.grid(row=1, column=0)
        self.quantity_entry = tk.Entry(self.inventory_frame)
        self.quantity_entry.grid(row=1, column=1)

        self.price_label = tk.Label(self.inventory_frame, text="Price:")
        self.price_label.grid(row=2, column=0)
        self.price_entry = tk.Entry(self.inventory_frame)
        self.price_entry.grid(row=2, column=1)

        self.add_button = tk.Button(self.inventory_frame, text="Add Product", command=self.add_product)
        self.add_button.grid(row=3, column=0)

        self.update_button = tk.Button(self.inventory_frame, text="Update Product", command=self.update_product)
        self.update_button.grid(row=3, column=1)

        self.delete_button = tk.Button(self.inventory_frame, text="Delete Product", command=self.delete_product)
        self.delete_button.grid(row=4, column=0)

        self.report_button = tk.Button(self.inventory_frame, text="Generate Report", command=self.generate_report)
        self.report_button.grid(row=4, column=1)

        self.low_stock_button = tk.Button(self.inventory_frame, text="Low Stock Alert", command=self.low_stock_alert)
        self.low_stock_button.grid(row=5, column=0, columnspan=2)

    def add_product(self):
        name = self.product_name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if not name or not quantity.isdigit() or not price.replace('.', '', 1).isdigit():
            messagebox.showerror("Input Error", "Please enter valid product details.")
            return

        with self.conn:
            try:
                self.conn.execute("INSERT INTO inventory (product_name, quantity, price) VALUES (?, ?, ?)",
                                  (name, int(quantity), float(price)))
                messagebox.showinfo("Success", "Product added successfully.")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Product already exists.")

        self.clear_entries()

    def update_product(self):
        name = self.product_name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if not name or (quantity and not quantity.isdigit()) or (price and not price.replace('.', '', 1).isdigit()):
            messagebox.showerror("Input Error", "Please enter valid product details.")
            return

        with self.conn:
            if quantity:
                self.conn.execute("UPDATE inventory SET quantity = ? WHERE product_name = ?",
                                  (int(quantity), name))
            if price:
                self.conn.execute("UPDATE inventory SET price = ? WHERE product_name = ?",
                                  (float(price), name))
            messagebox.showinfo("Success", "Product updated successfully.")

        self.clear_entries()

    def delete_product(self):
        name = self.product_name_entry.get()

        if not name:
            messagebox.showerror("Input Error", "Please enter a product name to delete.")
            return

        with self.conn:
            self.conn.execute("DELETE FROM inventory WHERE product_name = ?", (name,))
            messagebox.showinfo("Success", "Product deleted successfully.")

        self.clear_entries()

    def generate_report(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        rows = cursor.fetchall()

        report = "Inventory Report:\n"
        for row in rows:
            report += f"Product: {row[1]}, Quantity: {row[2]}, Price: ${row[3]:.2f}\n"

        messagebox.showinfo("Report", report)

    def low_stock_alert(self):
        threshold = 10  # Example threshold
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM inventory WHERE quantity < ?", (threshold,))
        rows = cursor.fetchall()

        alert = "Low Stock Alert:\n"
        for row in rows:
            alert += f"Product: {row[1]}, Quantity: {row[2]} units remaining.\n"

        if not rows:
            alert = "No products are below the low stock threshold."

        messagebox.showinfo("Low Stock Alert", alert)

    def clear_entries(self):
        self.product_name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)


if __name__ == "__main__":  # Fixed main entry point
    root = tk.Tk()
    app = InventoryManagementSystem(root)
    root.mainloop()
