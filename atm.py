class ATM:
    def _init_(self):
        self.balance = 1000  # Initial balance
        self.transaction_history = []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited: ${amount}")
            print(f"Deposited: ${amount}. New balance: ${self.balance}")
        else:
            print("Invalid deposit amount. Must be greater than 0.")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds!")
        elif amount <= 0:
            print("Invalid withdrawal amount. Must be greater than 0.")
        else:
            self.balance -= amount
            self.transaction_history.append(f"Withdrawn: ${amount}")
            print(f"Withdrawn: ${amount}. New balance: ${self.balance}")

    def check_balance(self):
        print(f"Current balance: ${self.balance}")

    def show_transaction_history(self):
        if not self.transaction_history:
            print("No transactions yet.")
        else:
            print("Transaction History:")
            for transaction in self.transaction_history:
                print(transaction)


def main():
    atm = ATM()
    while True:
        print("\nATM Interface")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transaction History")
        print("5. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            atm.check_balance()
        elif choice == '2':
            try:
                amount = float(input("Enter amount to deposit: "))
                atm.deposit(amount)
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
        elif choice == '3':
            try:
                amount = float(input("Enter amount to withdraw: "))
                atm.withdraw(amount)
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
        elif choice == '4':
            atm.show_transaction_history()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__== "_main_":
    main()