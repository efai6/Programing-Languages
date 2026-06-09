import unittest
from unittest.mock import Mock
from InvoiceRepository import InvoiceRepository
from Shop import Shop
from Invoice import Invoice
from Warehouse import Warehouse, OutOfStore


class ShopTests(unittest.TestCase):
    def test_while_buy_the_repository_add_should_be_called(self):
        spy_repository = Mock(InvoiceRepository)
        stub_warehouse = Mock(Warehouse)
        stub_warehouse.get_stock_info.return_value = {"quantity": 100, "price": 10}
        shop = Shop(spy_repository,stub_warehouse)
        shop.buy(customer="Jan", items_list= {"cukierki": {"quantity": 5, "price" : 10}})
        spy_repository.add.assert_called_once()

    def test_while_returning_goods_the_repository_returns_false_when_not_find(self):
        stub_repository = Mock(InvoiceRepository)
        dummy_warehouse = Mock(Warehouse)
        shop = Shop(stub_repository, dummy_warehouse)
        stub_repository.find_by_number.return_value = None
        result = shop.returning_goods(items_list= {"cukierki": {"quantity": 5, "price" : 10}}, invoice = Mock(Invoice))
        self.assertEqual(result, False)

    def test_buy_successful_with_fake_objects(self):
        fake_repo = InvoiceRepository([]) 
        fake_warehouse = Warehouse({"cukierki": {"quantity": 10, "price": 5.0}})
        shop = Shop(repository=fake_repo, warehouse=fake_warehouse)
        shop.buy(customer="Anna", items_list={"cukierki": {"quantity": 2}})
        self.assertEqual(len(fake_repo.data_source), 1)
        self.assertEqual(fake_warehouse.get_stock_info("cukierki")["quantity"], 8)

    def test_buy_raises_out_of_store_using_stub(self):
        dummy_repo = Mock(InvoiceRepository)
        stub_warehouse = Mock(Warehouse)
        stub_warehouse.get_stock_info.return_value = {"quantity": 1}
        stub_warehouse.remove_stock.side_effect = OutOfStore("cukierki", available=1, requested=5)
        shop = Shop(repository=dummy_repo, warehouse=stub_warehouse)
        with self.assertRaises(OutOfStore):
            shop.buy(customer="Jan", items_list={"cukierki": {"quantity": 5}})
    
    def test_returning_goods_calls_warehouse_add_stock_spy(self):
        """Spy: Перевіряємо, чи магазин правильно 'попросив' склад повернути товар."""
        stub_repo = Mock(InvoiceRepository)
        spy_warehouse = Mock(Warehouse)
        fake_invoice = Invoice(number=1, customer="Jan", items={"cukierki": {"quantity": 5}})
        stub_repo.find_by_number.return_value = fake_invoice
        shop = Shop(repository=stub_repo, warehouse=spy_warehouse)
        shop.returning_goods(items_list={"cukierki": {"quantity": 3}}, invoice=fake_invoice)
        spy_warehouse.add_stock.assert_called_once_with("cukierki", 3)

    def test_returning_goods_updates_repository(self):
        """Mock/Spy: Перевіряємо, чи викликається метод update() для збереження змін."""
        mock_repo = Mock(InvoiceRepository)
        dummy_warehouse = Mock(Warehouse)
        fake_invoice = Invoice(number=1, customer="Jan", items={"cukierki": {"quantity": 5}})
        mock_repo.find_by_number.return_value = fake_invoice
        shop = Shop(repository=mock_repo, warehouse=dummy_warehouse)
        shop.returning_goods(items_list={"cukierki": {"quantity": 2}}, invoice=fake_invoice)
        self.assertEqual(fake_invoice.items["cukierki"]["quantity"], 3)
        mock_repo.update.assert_called_once_with(fake_invoice)

    def test_returning_too_many_goods_raises_value_error(self):
        """Stub: Перевіряємо валідацію. Клієнт не може повернути більше, ніж купив."""
        stub_repo = Mock(InvoiceRepository)
        dummy_warehouse = Mock(Warehouse)
        
        fake_invoice = Invoice(number=1, customer="Jan", items={"cukierki": {"quantity": 2}})
        stub_repo.find_by_number.return_value = fake_invoice
        
        shop = Shop(repository=stub_repo, warehouse=dummy_warehouse)
        with self.assertRaises(ValueError):
            shop.returning_goods(items_list={"cukierki": {"quantity": 5}}, invoice=fake_invoice)

    def test_buy_does_not_add_invoice_if_warehouse_fails(self):
        """Dummy/Spy: Якщо склад викидає помилку, рахунок НЕ повинен створюватись."""
        spy_repo = Mock(InvoiceRepository)
        stub_warehouse = Mock(Warehouse)
        
        stub_warehouse.get_stock_info.return_value = {"quantity": 1}
        stub_warehouse.remove_stock.side_effect = OutOfStore("chleb", available=1, requested=2)
        
        shop = Shop(repository=spy_repo, warehouse=stub_warehouse)
        try:
            shop.buy(customer="Jan", items_list={"chleb": {"quantity": 2}})
        except OutOfStore:
            pass 
            
        spy_repo.add.assert_not_called()

    def test_returning_all_items_deletes_key_from_invoice(self):
        """Fake/Stub: Перевіряємо логіку очищення. Якщо повернуто все, товар зникає з чеку."""
        fake_invoice = Invoice(number=1, customer="Jan", items={"cukierki": {"quantity": 2}})
        stub_repo = Mock(InvoiceRepository)
        stub_repo.find_by_number.return_value = fake_invoice
        dummy_warehouse = Mock(Warehouse)
            
        shop = Shop(repository=stub_repo, warehouse=dummy_warehouse)
        
        shop.returning_goods(items_list={"cukierki": {"quantity": 2}}, invoice=fake_invoice)
        
        self.assertNotIn("cukierki", fake_invoice.items)


if __name__ == '__main__':
    unittest.main()