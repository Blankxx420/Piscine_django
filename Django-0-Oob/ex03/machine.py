from beverage import HotBeverage, Coffee, Tea, Chocolate, Cappuccino
import random

class CoffeeMachine:

    def __init__(self):
        self.number_served = 0
    
    class EmptyCup(HotBeverage):
        
        def __init__(self):
            super().__init__()
            self.name = "empty cup"
            self.price = 0.90

        def description(self):
            return "An empty cup?! Gimme my money back!"
    
    class BrokenMachineException(Exception):
        
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")
    
    def repair(self):
        self.number_served = 0
        print("The machine is repaired\n")

    def serve(self, beverage):
        
        if not isinstance(beverage, HotBeverage):
            raise TypeError("Error: Not a valid hot beverage!")

        if self.number_served > 10 :
            raise self.BrokenMachineException()
        
        self.number_served += 1
        if random.randint(0,1) == 1:
            return beverage
        else:
            return self.EmptyCup()


if __name__ == "__main__":
    machine = CoffeeMachine()
    
    beverage_stock = [Coffee(), Tea(), Chocolate(), Cappuccino()]
    
    for cycle in range(1, 3):
        print(f"=== STARTING CYCLE {cycle} ===")
        while True:
            try:
                choosen_beverage = random.choice(beverage_stock)
                
                result = machine.serve(choosen_beverage)
                print(f"[Served #{machine.number_served}] -> {result.name}")
                print(result)
                print("-" * 20)
                
            except CoffeeMachine.BrokenMachineException as e:
                print(f"\nEXCEPTION CAPTURED: {e}")
                break
        
        if cycle == 1:
            machine.repair()