# Account class
class Account:
    def __init__(self, name, number, balance):
        self.name = name
        self.number = number
        self.balance = balance
    def deposit(self, amount):
        self.balance += amount