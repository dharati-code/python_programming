class Category:
    
    def __init__(self, category, amount=0):
        self.category = category
        self.amount = amount

    def deposit(self, amount):
        self.amount += amount
        print(f"Deposit : $ {amount} added to {self.category}")

    def withdraw(self, amount):
        if self.check_balance(amount):
            self.amount -= amount
            print(f"Withdraw : $ {amount} withdrawn from {self.category}")
            return True
        else:
            print("Withdraw failed!!") 
            return False
        
    def balance(self):
        self.amount += 0
        print(f"Balance : You have $ {self.amount} in {self.category}")
        return self.amount
    
    def check_balance(self, amount):
        if self.amount <= amount:
            print(f"Check Balance : Your total balance in {self.category} category is {self.amount} which is less than or equal to {amount} you requested to check !")
            return False
        
        return True
    
    def transfer(self, amount, category):
        if not self.check_balance(amount):
            print(f"You dont have enough balance to transfer. You requested {amount} and you have {self.amount}")
            return False
        
        self.amount -= amount
        category.amount += amount
        
        print(f"Transfer : You are transfering {self.amount} from {self.category} to {category.category} with {category.amount} as original balance in {category.category}")
        return True
    

# test with some inputs 
instance =  Category("Food", 3000)
instance1 = Category("Car", 500)
instance2 = Category("Clothing", 200)
instance3 = Category("Travel", 100)

# Food category - balance, deposit and withdraw
print(instance.balance())
instance.deposit(300)
print(instance.balance())

instance.withdraw(200)
print(instance.balance())

print(instance.check_balance(300))

print(instance1.balance())

instance.transfer(100, instance2)
print(instance2.balance())

instance.transfer(100, instance3)
print(instance3.balance())

