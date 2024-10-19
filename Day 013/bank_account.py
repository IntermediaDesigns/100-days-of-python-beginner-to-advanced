import random
from datetime import datetime


class Transaction:
    def __init__(self, amount, transaction_type, description):
        self.amount = amount
        self.transaction_type = transaction_type
        self.description = description
        self.timestamp = datetime.now()

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.transaction_type}: ${self.amount:.2f} - {self.description}"


class BankAccount:
    def __init__(self, account_holder, account_number, initial_balance=0):
        self.account_holder = account_holder
        self.account_number = account_number
        self.balance = initial_balance
        self.transactions = []

    def deposit(self, amount, description="Deposit"):
        if amount > 0:
            self.balance += amount
            self.transactions.append(Transaction(amount, "Deposit", description))
            return True
        return False

    def withdraw(self, amount, description="Withdrawal"):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.transactions.append(Transaction(amount, "Withdrawal", description))
            return True
        return False

    def get_balance(self):
        return self.balance

    def print_statement(self):
        print(
            f"\nAccount Statement for {self.account_holder} (Account: {self.account_number})"
        )
        print(f"Current Balance: ${self.balance:.2f}")
        print("\nTransaction History:")
        for transaction in self.transactions:
            print(transaction)


class SavingsAccount(BankAccount):
    def __init__(
        self, account_holder, account_number, initial_balance=0, interest_rate=0.01
    ):
        super().__init__(account_holder, account_number, initial_balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.deposit(interest, "Interest")
        return interest


class CheckingAccount(BankAccount):
    def __init__(
        self, account_holder, account_number, initial_balance=0, overdraft_limit=100
    ):
        super().__init__(account_holder, account_number, initial_balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount, description="Withdrawal"):
        if 0 < amount <= (self.balance + self.overdraft_limit):
            self.balance -= amount
            self.transactions.append(Transaction(amount, "Withdrawal", description))
            return True
        return False


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}

    def create_account(self, account_type, account_holder, initial_balance=0):
        account_number = self.generate_account_number()
        if account_type == "savings":
            account = SavingsAccount(account_holder, account_number, initial_balance)
        elif account_type == "checking":
            account = CheckingAccount(account_holder, account_number, initial_balance)
        else:
            return None

        self.accounts[account_number] = account
        return account

    def generate_account_number(self):
        return "".join([str(random.randint(0, 9)) for _ in range(10)])

    def get_account(self, account_number):
        return self.accounts.get(account_number)


def main():
    bank = Bank("PyBank")

    while True:
        print("\nPyBank Account Simulator")
        print("1. Create a new account")
        print("2. Access existing account")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            account_holder = input("Enter account holder name: ")
            account_type = input("Enter account type (savings/checking): ").lower()
            initial_balance = float(input("Enter initial balance: "))

            account = bank.create_account(account_type, account_holder, initial_balance)
            if account:
                print(
                    f"Account created successfully. Your account number is: {account.account_number}"
                )
            else:
                print("Invalid account type. Please try again.")

        elif choice == "2":
            account_number = input("Enter your account number: ")
            account = bank.get_account(account_number)

            if account:
                while True:
                    print(f"\nWelcome, {account.account_holder}")
                    print("1. Check balance")
                    print("2. Deposit")
                    print("3. Withdraw")
                    print("4. Print statement")
                    print("5. Apply interest (Savings Account)")
                    print("6. Return to main menu")

                    action = input("Enter your choice (1-6): ")

                    if action == "1":
                        print(f"Your current balance is: ${account.get_balance():.2f}")
                    elif action == "2":
                        amount = float(input("Enter deposit amount: "))
                        if account.deposit(amount):
                            print("Deposit successful")
                        else:
                            print("Invalid deposit amount")
                    elif action == "3":
                        amount = float(input("Enter withdrawal amount: "))
                        if account.withdraw(amount):
                            print("Withdrawal successful")
                        else:
                            print("Insufficient funds or invalid amount")
                    elif action == "4":
                        account.print_statement()
                    elif action == "5":
                        if isinstance(account, SavingsAccount):
                            interest = account.apply_interest()
                            print(f"Interest applied: ${interest:.2f}")
                        else:
                            print("This feature is only available for Savings Accounts")
                    elif action == "6":
                        break
                    else:
                        print("Invalid choice. Please try again.")
            else:
                print("Account not found. Please try again.")

        elif choice == "3":
            print("Thank you for using PyBank Account Simulator. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
