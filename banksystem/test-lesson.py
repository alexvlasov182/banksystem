class BankAccount:
    def __init__(self, owner, amount=0, transaction: list = []) -> None:
        self.owner = owner
        self.amount = amount
        self.transaction = transaction

    def deposit_amount(self, amount):
        self.amount = amount
        self.transaction.append(f"Deposited {amount}")

    def withdraw_amount(self, amount):
        self.amount -= amount
        self.transaction.append(f"Withdraw -{amount}")

    def balance(self):
        print(f"Current Balance is {self.amount}")
        return self.amount

    def __str__(self) -> str:
        return f"{self.owner} Balance is {self.amount}"

    def __len__(self):
        return len(self.transaction)

    def __add__(self, other):
        owner = self.owner + " " + other.owner
        amount = self.amount + other.amount
        return BankAccount(owner, amount)


b = BankAccount(
    "John",
    1000,
)
print(b.amount)
print(b.withdraw_amount(100))
print(b.withdraw_amount(600))
print(b.amount)
b.balance()
print(len(b))
