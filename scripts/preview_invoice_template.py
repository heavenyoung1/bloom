"""
Скрипт для предпросмотра HTML шаблона платежного документа.
Запустите этот скрипт, чтобы сгенерировать HTML файл с тестовыми данными.
Затем откройте preview_invoice.html в браузере.
"""

from pathlib import Path
from datetime import date, datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape


def number_format(value: float) -> str:
    """Форматирование числа с пробелами и двумя знаками после запятой"""
    return f"{value:,.2f}".replace(",", " ").replace(".", ",")


def date_format(value: date) -> str:
    """Форматирование даты в русском формате"""
    months = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля",
        5: "мая", 6: "июня", 7: "июля", 8: "августа",
        9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }
    return f"{value.day} {months[value.month]} {value.year} года"


def main():
    # Путь к шаблону
    template_dir = Path(__file__).parent.parent / "templates"
    template_file = "payment/invoice_template.html"
    
    # Создаем Jinja2 окружение
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    # Добавляем фильтры
    env.filters['number_format'] = number_format
    env.filters['date_format'] = date_format
    
    # Загружаем шаблон
    template = env.get_template(template_file)
    
    # Тестовые данные (статичные - из PaymentDetail)
    payment_detail = {
        "attorney_name": "Адвокат Мефед Александр Иванович",
        "index_address": "241520",
        "address": "Брянский район, с. Супонево, ул. Чувиной, д. 55",
        "inn": "320700930330",
        "kpp": "0",
        "bank_recipient": "БРЯНСКОЕ ОТДЕЛЕНИЕ №8605 ПАО СБЕРБАНК",
        "bank_account": "40802810908000000092",
        "bik": "041501601",
        "correspondent_account": "30101810400000000601",
    }
    
    # Тестовые данные (динамические - из ClientPayment)
    payment = {
        "id": "250820251",
        "name": "Оплата по соглашению от 27 мая 2024 года за предоставление юридической помощи",
        "paid": 30000.00,
        "paid_str": "Тридцать тысяч рублей 00 копеек",
        "pade_date": date(2025, 8, 25),
        "condition": "Оплата производится в течение 5-ти (пяти) дней с даты выставления счета. Зачисление происходит в течение 3-х (рабочих дней).",
    }
    
    # Тестовые данные клиента
    client = {
        "name": 'ООО "Служба эксплуатации САКС"',
    }
    
    # Рендерим шаблон
    html_content = template.render(
        payment_detail=payment_detail,
        payment=payment,
        client=client
    )
    
    # Сохраняем результат
    output_file = Path(__file__).parent.parent / "preview_invoice.html"
    output_file.write_text(html_content, encoding='utf-8')
    
    print("Шаблон успешно сгенерирован!")
    print(f"Файл сохранен: {output_file.absolute()}")
    print(f"\nОткройте файл в браузере для просмотра:")
    print(f"   {output_file.absolute()}")
    print(f"\nИли просто дважды кликните на файл preview_invoice.html")


if __name__ == "__main__":
    main()

