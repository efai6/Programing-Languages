from abc import ABC

class OutOfStore(Exception):
    def __init__(self, item_name, available, requested):
        self.item_name = item_name
        self.available = available
        self.requested = requested
        super().__init__(
            f"Nie wystarczająca ilość towaru '{item_name}' w magazynie! "
            f"Wymagano: {requested} sztuk, jest dostępnych: {available} sztuk."
        )


class Warehouse(ABC):
    def __init__(self, initial_stock=None):
        if initial_stock is None:
            self.__stock = {}
        else:
            self.__stock = initial_stock

    def add_stock(self, item_name, quantity, price=0.0):
        if quantity <= 0:
            raise ValueError("Ilość towatu ma być większa od 0!")
            
        if item_name in self.__stock:
            self.__stock[item_name]["quantity"] += quantity
            if price > 0:
                self.__stock[item_name]["price"] = price
        else:
            self.__stock[item_name] = {"quantity": quantity, "price": price}

    def remove_stock(self, item_name, quantity):
        if quantity <= 0:
            raise ValueError("Ilość towaru do usunięcia ma być większa od zera!")

        # Sprawdzamy obecność w magazynie
        if item_name not in self.__stock or self.__stock[item_name]["quantity"] == 0:
            raise OutOfStore(item_name, available=0, requested=quantity)

        available_quantity = self.__stock[item_name]["quantity"]

        # Sprawdzamy ilość
        if available_quantity < quantity:
            raise OutOfStore(item_name, available=available_quantity, requested=quantity)

        self.__stock[item_name]["quantity"] -= quantity

    def get_stock_info(self, item_name):
        return self.__stock.get(item_name, {"quantity": 0, "price": 0.0})

    @property
    def stock(self):
        return self.__stock