# PDF Generator - Заполнение шаблонов по координатам

## Структура

```
backend/infrastructure/pdf/
├── __init__.py
├── pdf_generator.py          # Сервис для генерации PDF
├── config/
│   └── invoice_fields.json   # Конфиг с координатами полей
└── README.md                 # Эта инструкция
```

## Как найти координаты полей в PDF

### Вариант 1: Adobe Acrobat Pro (рекомендуется)
1. Откройте PDF в Adobe Acrobat Pro
2. Инструменты → Подготовка форм → Редактировать
3. Добавьте текстовые поля там, где нужно вставить данные
4. Правой кнопкой на поле → Свойства → Положение
5. Запишите координаты X, Y, ширина, высота

### Вариант 2: Онлайн инструменты
- https://www.pdfescape.com/ - позволяет добавлять поля и видеть координаты
- https://www.sejda.com/pdf-editor - онлайн редактор PDF

### Вариант 3: Python скрипт для определения координат
```python
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Создайте тестовый PDF с координатной сеткой
c = canvas.Canvas("coordinate_grid.pdf", pagesize=A4)
page_height = A4[1]

# Рисуем сетку
for x in range(0, int(A4[0]), 50):
    c.line(x, 0, x, page_height)
    c.drawString(x, page_height - 20, str(x))

for y in range(0, int(page_height), 50):
    c.line(0, y, A4[0], y)
    c.drawString(10, page_height - y, str(y))

c.save()
```

Наложите этот PDF поверх вашего шаблона, чтобы увидеть координаты.

## Формат конфиг-файла

```json
{
  "template_name": "invoice_template",
  "template_path": "templates/payment/invoice_template.pdf",
  "page_number": 0,
  "fields": {
    "static": {
      "inn": {
        "x": 100,           // X координата (от левого края)
        "y": 700,           // Y координата (от нижнего края)
        "width": 150,       // Ширина поля (необязательно)
        "height": 15,       // Высота поля (необязательно)
        "font_size": 10,    // Размер шрифта
        "font_name": "Helvetica",  // Имя шрифта
        "align": "left"     // Выравнивание: left, right, center
      }
    },
    "dynamic": {
      "name": {
        "x": 50,
        "y": 500,
        "width": 400,
        "height": 30,
        "font_size": 11,
        "font_name": "Helvetica"
      }
    }
  }
}
```

## Важные замечания

### Система координат PDF
- **Начало координат**: левый нижний угол страницы (0, 0)
- **Ось X**: растет вправо
- **Ось Y**: растет вверх
- **Единица измерения**: точки (points), 1 точка = 1/72 дюйма
- **Размер A4**: 595 x 842 точек (ширина x высота)

### Шрифты
Доступные шрифты в ReportLab:
- `Helvetica` (по умолчанию)
- `Helvetica-Bold`
- `Helvetica-Oblique`
- `Times-Roman`
- `Times-Bold`
- `Courier`
- `Courier-Bold`

### Советы
1. **Начните с примерных координат** - можно скорректировать позже
2. **Используйте тестовый PDF** - создайте тестовый документ для проверки
3. **Учитывайте размер текста** - длинный текст может не поместиться
4. **Проверяйте на реальных данных** - координаты могут отличаться для разных значений

## Использование

```python
from backend.infrastructure.pdf import PDFGenerator
from backend.domain.entities.payment import ClientPayment
from backend.domain.entities.payment_detail import PaymentDetail

# Создаем генератор
generator = PDFGenerator()

# Генерируем PDF
pdf_bytes = await generator.fill_invoice_template(
    payment=payment_entity,
    payment_detail=payment_detail_entity
)

# Сохраняем или отправляем
with open("invoice.pdf", "wb") as f:
    f.write(pdf_bytes)
```

## Отладка координат

Если текст не попадает в нужное место:

1. **Проверьте систему координат** - убедитесь, что используете координаты от нижнего края
2. **Проверьте размер страницы** - A4 = 595 x 842 точек
3. **Используйте тестовые значения** - вставьте простой текст для проверки
4. **Проверьте шрифт** - некоторые шрифты могут иметь разную высоту

## Пример тестового скрипта

Создайте файл `test_coordinates.py`:

```python
from backend.infrastructure.pdf import PDFGenerator
from datetime import date

# Создайте тестовые объекты
class TestPayment:
    id = 1
    name = "Тестовая услуга"
    paid = 30000.00
    paid_str = "Тридцать тысяч рублей"
    pade_date = date(2025, 8, 25)
    paid_deadline = None
    taxable = False
    condition = None

class TestPaymentDetail:
    inn = "320700930330"
    kpp = "0"
    index_address = "241520"
    address = "Брянский район, с. Супонево"
    bank_account = "40802810908000000092"
    correspondent_account = "30101810400000000601"
    bik = "041501601"
    bank_recipient = "СБЕРБАНК"

# Генерируем тестовый PDF
generator = PDFGenerator()
pdf_bytes = await generator.fill_invoice_template(
    payment=TestPayment(),
    payment_detail=TestPaymentDetail()
)

with open("test_invoice.pdf", "wb") as f:
    f.write(pdf_bytes)
```



