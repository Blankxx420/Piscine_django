class HotBeverage:

    def __init__(self):
        self.price = 0.30
        self.name = "hot beverage"

    def description(self):
        return "Just some hot water in a cup."
    
    def __str__(self):
        return (f"name : {self.name}\n"
                f"price : {self.price:.2f}\n"
                f"description : {self.description()}")
    
class Coffee(HotBeverage):

    def __init__(self):
        super().__init__()
        self.price = 0.40
        self.name = "coffee"
    
    def description(self):
        return "A coffee, to stay awake."

class Tea(HotBeverage):

    def __init__(self):
        super().__init__()
        self.name = "tea"
    
class Chocolate(HotBeverage):

    def __init__(self):
        super().__init__()
        self.price = 0.50
        self.name = "chocolate"
    
    def description(self):
        return "Chocolate, sweet chocolate..."

class Cappuccino(HotBeverage):

    def __init__(self):
        super().__init__()
        self.price = 0.45
        self.name = "cappuccino"
    
    def description(self):
        return "Un po' di Italia nella sua tazza!"
    

if __name__ == "__main__":
    print("=== INSTANTIATION AND OUTPUT TESTS ===")
    
    generic_beverage = HotBeverage()
    print("--- HotBeverage ---")
    print(generic_beverage)
    print()

    my_coffee = Coffee()
    print("--- Coffee ---")
    print(my_coffee)
    print()

    my_tea = Tea()
    print("--- Tea ---")
    print(my_tea)
    print()

    my_chocolate = Chocolate()
    print("--- Chocolate ---")
    print(my_chocolate)
    print()

    my_cappuccino = Cappuccino()
    print("--- Cappuccino ---")
    print(my_cappuccino)
    print()

    print("=== INHERITANCE AND TYPE VERIFICATION TESTS ===")
    
    beverages = {
        "Coffee": my_coffee,
        "Tea": my_tea,
        "Chocolate": my_chocolate,
        "Cappuccino": my_cappuccino
    }

    for name, instance in beverages.items():
        is_subclass = isinstance(instance, HotBeverage)
        print(f"Is {name} an instance of HotBeverage? -> {is_subclass}")

    print("\nAll tests completed successfully!")