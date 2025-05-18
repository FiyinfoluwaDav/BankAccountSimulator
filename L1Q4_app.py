import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import json
import os

# File paths for storing account data
ACTIVE_ACCOUNTS_FILE = 'active_accounts.json'
DELETED_ACCOUNTS_FILE = 'deleted_accounts.json'

class CustomerAccount:
    def __init__(self, account_number, surname, firstname, password):
        self.account_number = account_number
        self.surname = surname
        self.firstname = firstname
        self.password = password
        self.balance = 0.0

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            return False
        self.balance -= amount
        return True

class BankSystem:
    def __init__(self):
        self.accounts = self.load_data(ACTIVE_ACCOUNTS_FILE)
        self.deleted_accounts = self.load_data(DELETED_ACCOUNTS_FILE)

    def load_data(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                return json.load(file)
        return {}

    def save_data(self, file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def generate_account_number(self):
        while True:
            acc_num = str(random.randint(1000000000, 9999999999))
            if acc_num not in self.accounts and acc_num not in self.deleted_accounts:
                return acc_num

    def create_account(self, surname, firstname, password):
        acc_num = self.generate_account_number()
        account = CustomerAccount(acc_num, surname, firstname, password)
        self.accounts[acc_num] = account.__dict__
        self.save_data(ACTIVE_ACCOUNTS_FILE, self.accounts)
        return acc_num

    def login(self, account_number, password):
        account = self.accounts.get(account_number)
        if account and account['password'] == password:
            return CustomerAccount(account_number, account['surname'], account['firstname'], account['password'])
        return None

    def delete_account(self, account_number):
        if account_number in self.accounts:
            self.deleted_accounts[account_number] = self.accounts.pop(account_number)
            self.save_data(ACTIVE_ACCOUNTS_FILE, self.accounts)
            self.save_data(DELETED_ACCOUNTS_FILE, self.deleted_accounts)
            return True
        return False

    def recover_account(self, account_number, password):
        account = self.deleted_accounts.get(account_number)
        if account and account['password'] == password:
            self.accounts[account_number] = account
            del self.deleted_accounts[account_number]
            self.save_data(ACTIVE_ACCOUNTS_FILE, self.accounts)
            self.save_data(DELETED_ACCOUNTS_FILE, self.deleted_accounts)
            return True
        return False

class BankApp:
    def __init__(self, root):
        self.bank_system = BankSystem()
        self.root = root
        self.root.title("Fiyinfoluwa Microfinance Bank")
        self.root.geometry("400x500")
        self.current_user = None
        self.main_menu()

    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_window()
        self.root.configure(bg="#007bff")

        header_label = tk.Label(self.root, text="Welcome to Fiyinfoluwa Microfinance Bank", 
                              font=("Arial", 16, "bold"), fg="white", bg="#007bff")
        header_label.pack(pady=20)

        frame = tk.Frame(self.root, bg="#007bff")
        frame.pack(pady=20)

        buttons = [
            ("Create Account", "#28a745", self.create_account_screen),
            ("Login", "#ffc107", self.login_screen),
            ("Recover Account", "#17a2b8", self.recover_account_screen),
            ("Exit", "#dc3545", self.root.quit)
        ]

        for text, color, command in buttons:
            tk.Button(frame, text=text, width=20, command=command, bg=color, fg="white",
                      font=("Arial", 12, "bold"), relief="solid", bd=2, padx=10, pady=5).pack(pady=10)

    def create_account_screen(self):
        self.clear_window()

        header_label = tk.Label(self.root, text="Create Account", font=("Arial", 16, "bold"), 
                              fg="white", bg="#007bff")
        header_label.pack(pady=20)

        frame = tk.Frame(self.root, bg="#007bff")
        frame.pack(pady=20)

        self.surname_var = tk.StringVar()
        self.firstname_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(frame, text="Surname:", font=("Arial", 12, "bold"), fg="white", bg="#007bff").pack()
        tk.Entry(frame, textvariable=self.surname_var, font=("Arial", 12)).pack(pady=5)

        tk.Label(frame, text="Firstname:", font=("Arial", 12, "bold"), fg="white", bg="#007bff").pack()
        tk.Entry(frame, textvariable=self.firstname_var, font=("Arial", 12)).pack(pady=5)

        tk.Label(frame, text="Password:", font=("Arial", 12, "bold"), fg="white", bg="#007bff").pack()
        tk.Entry(frame, textvariable=self.password_var, show="*", font=("Arial", 12)).pack(pady=5)

        tk.Button(frame, text="Create Account", command=self.create_account, bg="#28a745", fg="white",
                 font=("Arial", 12, "bold"), relief="solid", bd=2, padx=10, pady=5).pack(pady=10)
        tk.Button(frame, text="Back", command=self.main_menu, bg="#dc3545", fg="white",
                 font=("Arial", 12, "bold"), relief="solid", bd=2, padx=10, pady=5).pack(pady=10)

    def create_account(self):
        surname = self.surname_var.get()
        firstname = self.firstname_var.get()
        password = self.password_var.get()

        if not surname or not firstname or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        account_number = self.bank_system.create_account(surname, firstname, password)
        messagebox.showinfo("Account Created", f"Account created! Your Account Number is: {account_number}")
        self.main_menu()

    def login_screen(self):
        self.clear_window()

        header_label = tk.Label(self.root, text="Login", font=("Arial", 16, "bold"), 
                              fg="white", bg="#007bff")
        header_label.pack(pady=20)

        frame = tk.Frame(self.root, bg="#007bff")
        frame.pack(pady=20)

        self.acc_num_var = tk.StringVar()
        self.pass_var = tk.StringVar()

        tk.Label(frame, text="Account Number:", font=("Arial", 12, "bold"), fg="white", bg="#007bff").pack()
        tk.Entry(frame, textvariable=self.acc_num_var, font=("Arial", 12)).pack(pady=5)

        tk.Label(frame, text="Password:", font=("Arial", 12, "bold"), fg="white", bg="#007bff").pack()
        tk.Entry(frame, textvariable=self.pass_var, show="*", font=("Arial", 12)).pack(pady=5)

        tk.Button(frame, text="Login", command=self.login, bg="#ffc107", fg="white",
                 font=("Arial", 12, "bold"), relief="solid", bd=2, padx=10, pady=5).pack(pady=10)
        tk.Button(frame, text="Back", command=self.main_menu, bg="#dc3545", fg="white",
                 font=("Arial", 12, "bold"), relief="solid", bd=2, padx=10, pady=5).pack(pady=10)

    def login(self):
        account_number = self.acc_num_var.get()
        password = self.pass_var.get()

        self.current_user = self.bank_system.login(account_number, password)

        if self.current_user:
            self.user_dashboard()
        else:
            messagebox.showerror("Error", "Invalid account number or password.")

    def user_dashboard(self):
        self.clear_window()

        header_label = tk.Label(self.root, text="Dashboard", font=("Arial", 16, "bold"), 
                              fg="white", bg="#007bff")
        header_label.pack(pady=20)

        frame = tk.Frame(self.root, bg="#007bff")
        frame.pack(pady=20)

        tk.Label(frame, text=f"Welcome {self.current_user.firstname} {self.current_user.surname}", 
                font=("Arial", 12, "bold"), fg="white", bg="#007bff").pack(pady=10)

        buttons = [
            ("Deposit", "#28a745", self.deposit_screen),
            ("Withdraw", "#ffc107", self.withdraw_screen),
            ("View Balance", "#007bff", self.view_balance),
            ("Delete Account", "#dc3545", self.delete_account),
            ("Logout", "#6c757d", self.logout)
        ]

        for text, color, command in buttons:
            tk.Button(frame, text=text, width=20, command=command, bg=color, fg="white",
                      font=("Arial", 12, "bold"), relief="solid", bd=2, padx=10, pady=5).pack(pady=10)

    def logout(self):
        self.current_user = None
        self.main_menu()

    def deposit_screen(self):
        self.clear_window()

        header_label = tk.Label(self.root, text="Deposit", font=("Arial", 16, "bold"), 
                              fg="white", bg="#007bff")
        header_label.pack(pady=20)

        frame = tk.Frame(self.root, bg="#007bff")
        frame.pack(pady=20)

        self.deposit_amount_var = tk.DoubleVar()

        tk.Label(frame, text="Enter Amount to Deposit:", font=("Arial", 12, "bold"), 
                fg="white", bg="#007bff").pack()
        tk.Entry(frame, textvariable=self.deposit_amount_var, font=("Arial", 12)).pack(pady=5)

        tk.Button(frame, text="Deposit", command=self.deposit, bg="#28a745", fg="white",
                 font=("Arial", 12, "bold"), relief="solid", bd=2, padx=10, pady=5).pack(pady=10)
        tk.Button(frame, text="Back", command=self.user_dashboard, bg="#dc3545", fg="white",
                 font=("Arial", 12, "bold"), relief="solid", bd=2, padx=10, pady=5).pack(pady=10)

    def deposit(self):
        password = simpledialog.askstring("Password Confirmation", "Enter your password:", show='*')
        if password != self.current_user.password:
            messagebox.showerror("Error", "Incorrect password.")
            return

        amount = self.deposit_amount_var.get()
        if amount <= 0:
            messagebox.showerror("Error", "Deposit amount must be greater than zero.")
            return

        self.current_user.deposit(amount)
        self.bank_system.accounts[self.current_user.account_number] = self.current_user.__dict__
        self.bank_system.save_data(ACTIVE_ACCOUNTS_FILE, self.bank_system.accounts)
        messagebox.showinfo("Success", f"Deposited {amount}. New Balance: {self.current_user.balance}")
        self.user_dashboard()

    def withdraw_screen(self):
        self.clear_window()

        header_label = tk.Label(self.root, text="Withdraw", font=("Arial", 16, "bold"), 
                              fg="white", bg="#007bff")
        header_label.pack(pady=20)

        frame = tk.Frame(self.root, bg="#007bff")
        frame.pack(pady=20)

        self.withdraw_amount_var = tk.DoubleVar()

        tk.Label(frame, text="Enter Amount to Withdraw:", font=("Arial", 12, "bold"), 
                fg="white", bg="#007bff").pack()
        tk.Entry(frame, textvariable=self.withdraw_amount_var, font=("Arial", 12)).pack(pady=5)

        tk.Button(frame, text="Withdraw", command=self.withdraw, bg="#ffc107", fg="white",
                 font=("Arial", 12, "bold"), relief="solid", bd=2, padx=10, pady=5).pack(pady=10)
        tk.Button(frame, text="Back", command=self.user_dashboard, bg="#dc3545", fg="white",
                 font=("Arial", 12, "bold"), relief="solid", bd=2, padx=10, pady=5).pack(pady=10)

    def withdraw(self):
        password = simpledialog.askstring("Password Confirmation", "Enter your password:", show='*')
        if password != self.current_user.password:
            messagebox.showerror("Error", "Incorrect password.")
            return

        amount = self.withdraw_amount_var.get()
        if amount <= 0:
            messagebox.showerror("Error", "Withdrawal amount must be greater than zero.")
            return

        if not self.current_user.withdraw(amount):
            messagebox.showerror("Error", "Insufficient funds.")
            return

        self.bank_system.accounts[self.current_user.account_number] = self.current_user.__dict__
        self.bank_system.save_data(ACTIVE_ACCOUNTS_FILE, self.bank_system.accounts)
        messagebox.showinfo("Success", f"Withdrew {amount}. New Balance: {self.current_user.balance}")
        self.user_dashboard()

    def view_balance(self):
        messagebox.showinfo("Balance", f"Your current balance is: {self.current_user.balance}")

    def delete_account(self):
        password = simpledialog.askstring("Password Confirmation", "Enter your password:", show='*')
        if password != self.current_user.password:
            messagebox.showerror("Error", "Incorrect password.")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete your account?"):
            if self.bank_system.delete_account(self.current_user.account_number):
                messagebox.showinfo("Deleted", "Account deleted successfully.")
                self.logout()
            else:
                messagebox.showerror("Error", "Error deleting account.")

    def recover_account_screen(self):
        self.clear_window()

        header_label = tk.Label(self.root, text="Recover Account", font=("Arial", 16, "bold"), 
                              fg="white", bg="#007bff")
        header_label.pack(pady=20)

        frame = tk.Frame(self.root, bg="#007bff")
        frame.pack(pady=20)

        self.recover_acc_num_var = tk.StringVar()
        self.recover_pass_var = tk.StringVar()

        tk.Label(frame, text="Account Number:", font=("Arial", 12, "bold"), fg="white", bg="#007bff").pack()
        tk.Entry(frame, textvariable=self.recover_acc_num_var, font=("Arial", 12)).pack(pady=5)

        tk.Label(frame, text="Password:", font=("Arial", 12, "bold"), fg="white", bg="#007bff").pack()
        tk.Entry(frame, textvariable=self.recover_pass_var, show="*", font=("Arial", 12)).pack(pady=5)

        tk.Button(frame, text="Recover Account", command=self.recover_account, bg="#17a2b8", fg="white",
                 font=("Arial", 12, "bold"), relief="solid", bd=2, padx=10, pady=5).pack(pady=10)
        tk.Button(frame, text="Back", command=self.main_menu, bg="#dc3545", fg="white",
                 font=("Arial", 12, "bold"), relief="solid", bd=2, padx=10, pady=5).pack(pady=10)

    def recover_account(self):
        account_number = self.recover_acc_num_var.get()
        password = self.recover_pass_var.get()

        if not account_number or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        if self.bank_system.recover_account(account_number, password):
            messagebox.showinfo("Success", "Account recovered successfully!")
            self.main_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials or account not found in deleted accounts.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()