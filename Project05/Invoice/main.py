from InvoiceRepository import InvoiceRepository
from Shop import Shop
from Invoice import Invoice

def main():
    print("=== ЗАПУСК ПРОГРАМИ ОБСЛУГОВУВАННЯ МАГАЗИНУ ===")
    
    # 1. Ініціалізуємо репозиторій рахунків (порожнє сховище в пам'яті)
    repository = InvoiceRepository()
    
    # 2. Створюємо магазин і передаємо йому наше сховище
    shop = Shop(repository)
    
    print(f"\nПоточна кількість рахунків у базі: {len(repository.data_source)}")
    
    print("\n--- Симуляція 1: Клієнт Jan купує цукерки ---")
    try:
        # Метод buy автоматично намагається згенерувати наступний номер рахунку
        invoice_jan = shop.buy(customer="Jan", items_list=["cukierki"])
        print(f"🎉 Покупка успішна! Створено рахунок: {invoice_jan}")
    except IndexError:
        print("❌ Помилка: Спроба отримати елемент з порожнього списку!")
        print("💡 Це сталося через баг у методі get_next_number() класу InvoiceRepository.")
        print("Оскільки список рахунків порожній, умова `1 if len(self.__data_source)` спрацювала некоректно,")
        print("і програма спробувала звернутися до індексу [-1] у порожньому списку.")
        print("\nЩоб програма запрацювала далі, застосуємо тимчасове виправлення прямо в цьому сценарії.")
        
        # Тимчасовий обхід багу для демонстрації (якщо ти ще не правив оригінальний файл)
        print("Тимчасово додаємо тестовий рахунок вручну для обходу багу...")
        test_invoice = Invoice(number=1, customer="Test", items=["test_item"])
        repository.add(test_invoice)
        
        # Спробуємо купити ще раз
        invoice_jan = shop.buy(customer="Jan", items_list=["cukierki"])
        print(f"🎉 Тепер покупка успішна (завдяки наявності тестового рахунку): {invoice_jan}")

    # 3. Перевіряємо, які рахунки зараз є в репозиторії
    print("\n--- Поточний стан репозиторію рахунків ---")
    for inv in repository.data_source:
        print(f"- Рахунок №{inv.number}: Клієнт: {inv.customer}, Товари: {inv.items}")

    print("\n--- Симуляція 2: Повернення товару ---")
    # Спробуємо повернути товар за рахунком, який ми щойно створили для Jan
    print(f"Намагаємось повернути рахунок №{invoice_jan.number}...")
    success = shop.returning_goods(invoice_jan)
    
    if success:
        print("✅ Товари успішно повернуто, рахунок видалено з репозиторію.")
    else:
        print("❌ Не вдалося знайти такий рахунок для повернення.")

    # 4. Фінальна перевірка репозиторію
    print(f"\nВсього рахунків у базі в кінці роботи: {len(repository.data_source)}")

if __name__ == "__main__":
    main()