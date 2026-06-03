from abc import ABC
from Invoice import Invoice
from Warehouse import Warehouse


class Shop(ABC):
    def __init__(self, repository=None, warehouse = None):
        self.__invoice_repository = repository
        self.__warehouse = warehouse

    def buy(self, customer, items_list):
        for item in items_list:
            needed = items_list[item]["quantity"]
            available = self.warehouse.get_stock_info(item)["quantity"]
            if available < needed:
                self.warehouse.remove_stock(item, needed)
        
        for item in items_list:
            self.warehouse.remove_stock(item, items_list[item]["quantity"])
        invoice = Invoice(number=self.invoice_repository.get_next_number(), customer=customer, items=items_list)
        self.invoice_repository.add(invoice)
        return invoice

    def returning_goods(self, items_list, invoice):
        found_invoice = self.invoice_repository.find_by_number(invoice.number)

        if found_invoice:
            for item in items_list:
                qty_to_return = items_list[item]["quantity"]
                if item in found_invoice.items:
                    current_qty_in_invoice = found_invoice.items[item]["quantity"]
                    if qty_to_return > current_qty_in_invoice:
                        raise ValueError(f"Nie można zwrócić większej ilości towarów niż zakupiono {qty_to_return} szt. '{item}', zakupiono: {current_qty_in_invoice} szt.")

                    self.warehouse.add_stock(item, qty_to_return)

                    found_invoice.items[item]["quantity"] -= qty_to_return

                    if found_invoice.items[item]["quantity"] == 0:
                        del found_invoice.items[item]


            self.invoice_repository.update(found_invoice)
            return True
        else:
            return False

    @property
    def invoice_repository(self):
        return self.__invoice_repository
    
    @property
    def warehouse(self):
        return self.__warehouse