"""
Скрипт для создания координатной сетки PDF.
Создает PDF с сеткой координат, который можно наложить на ваш шаблон
для определения координат полей.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import red, blue, black
from pathlib import Path


def create_coordinate_grid(output_path: str = "coordinate_grid.pdf"):
    """
    Создает PDF с координатной сеткой для определения позиций полей.

    Args:
        output_path: Путь для сохранения PDF файла
    """
    c = canvas.Canvas(output_path, pagesize=A4)
    page_width, page_height = A4

    # Основные линии сетки (каждые 50 точек)
    c.setStrokeColor(black)
    c.setLineWidth(0.5)

    # Вертикальные линии
    for x in range(0, int(page_width), 50):
        c.line(x, 0, x, page_height)
        # Подписи координат сверху
        c.setFont("Helvetica", 8)
        c.drawString(x + 2, page_height - 15, str(x))

    # Горизонтальные линии
    for y in range(0, int(page_height), 50):
        c.line(0, y, page_width, y)
        # Подписи координат слева
        c.setFont("Helvetica", 8)
        c.drawString(5, y + 2, str(y))

    # Более тонкие линии (каждые 10 точек) для точности
    c.setLineWidth(0.2)
    c.setStrokeColor(blue)

    for x in range(0, int(page_width), 10):
        if x % 50 != 0:  # Пропускаем основные линии
            c.line(x, 0, x, page_height)

    for y in range(0, int(page_height), 10):
        if y % 50 != 0:  # Пропускаем основные линии
            c.line(0, y, page_width, y)

    # Центральные линии (красные)
    c.setStrokeColor(red)
    c.setLineWidth(1)
    center_x = page_width / 2
    center_y = page_height / 2
    c.line(center_x, 0, center_x, page_height)
    c.line(0, center_y, page_width, center_y)

    # Подписи в центре
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(red)
    c.drawString(center_x + 5, page_height - 20, f"Center X: {center_x}")
    c.drawString(10, center_y + 5, f"Center Y: {center_y}")

    # Информация о размерах страницы
    c.setFillColor(black)
    c.setFont("Helvetica", 10)
    info_text = [
        f"Page size: {int(page_width)} x {int(page_height)} points",
        "Coordinate system: (0,0) at bottom-left",
        "Y-axis grows upward",
        "1 point = 1/72 inch",
    ]
    y_pos = 30
    for line in info_text:
        c.drawString(10, y_pos, line)
        y_pos -= 15

    c.save()
    print(f"✅ Координатная сетка создана: {output_path}")
    print(f"📄 Откройте этот файл и наложите на ваш PDF шаблон")
    print(f"💡 Используйте прозрачный режим в PDF просмотрщике для наложения")


def overlay_grid_on_template(
    template_path: str, output_path: str = "template_with_grid.pdf"
):
    """
    Накладывает координатную сетку на существующий PDF шаблон.

    Args:
        template_path: Путь к вашему PDF шаблону
        output_path: Путь для сохранения результата
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter

        # Читаем шаблон
        template_reader = PdfReader(template_path)

        # Создаем координатную сетку
        grid_path = "temp_grid.pdf"
        create_coordinate_grid(grid_path)
        grid_reader = PdfReader(grid_path)

        # Объединяем
        writer = PdfWriter()

        for page_num, page in enumerate(template_reader.pages):
            # Копируем страницу шаблона
            writer.add_page(page)

            # Накладываем сетку
            if page_num < len(grid_reader.pages):
                grid_page = grid_reader.pages[page_num]
                writer.pages[page_num].merge_page(grid_page)

        # Сохраняем результат
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        # Удаляем временный файл
        Path(grid_path).unlink()

        print(f"✅ Шаблон с координатной сеткой создан: {output_path}")
        print(f"📄 Откройте этот файл, чтобы увидеть координаты на вашем шаблоне")

    except ImportError:
        print("❌ PyPDF2 не установлен. Установите: uv pip install PyPDF2")
    except FileNotFoundError:
        print(f"❌ Шаблон не найден: {template_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Если передан путь к шаблону, накладываем сетку на него
        template_path = sys.argv[1]
        overlay_grid_on_template(template_path)
    else:
        # Иначе просто создаем координатную сетку
        create_coordinate_grid()
        print("\n💡 Для наложения сетки на ваш шаблон запустите:")
        print(
            "   python scripts/create_coordinate_grid.py templates/payment/invoice_template.pdf"
        )
