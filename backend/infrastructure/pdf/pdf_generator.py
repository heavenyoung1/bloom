'''
Сервис для заполнения PDF шаблонов по координатам.
Использует pypdf для работы с PDF файлами.
'''

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import date, datetime

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO

from backend.core.logger import logger
from backend.core.exceptions import ValidationException
from backend.core.settings import settings


class PDFGenerator:
    '''
    Генератор PDF документов на основе шаблонов с заполнением по координатам.

    Шаблон PDF берется из настройки FILE_STORAGE_TEMPLATE в .env файле.
    Координаты полей берутся из конфига invoice_fields.json.

    Процесс:
    1. Копируется шаблон PDF (универсальный для всех юристов)
    2. Создается overlay PDF с данными по координатам из конфига
    3. Overlay накладывается на шаблон
    4. Возвращается готовый PDF документ

    Использование:
        generator = PDFGenerator()
        pdf_bytes = generator.fill_invoice_template(
            payment=payment_entity,
            payment_detail=payment_detail_entity
        )
    '''

    def __init__(self, config_path: Optional[Path] = None):
        '''
        Args:
            config_path: Путь к конфиг-файлу с координатами полей.
                        По умолчанию: backend/infrastructure/pdf/config/invoice_fields.json
        '''
        if config_path is None:
            base_dir = Path(__file__).parent.parent.parent
            config_path = (
                base_dir / 'infrastructure' / 'pdf' / 'config' / 'invoice_fields.json'
            )

        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.base_dir = Path(__file__).parent.parent.parent.parent

    def _load_config(self) -> Dict[str, Any]:
        '''Загружает конфигурацию полей из JSON файла.'''
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            logger.info(f'Конфигурация PDF загружена: {self.config_path}')
            return config
        except FileNotFoundError:
            logger.error(f'Конфиг файл не найден: {self.config_path}')
            raise FileNotFoundError(f'Конфиг файл не найден: {self.config_path}')
        except json.JSONDecodeError as e:
            logger.error(f'Ошибка парсинга JSON конфига: {e}')
            raise ValidationException(f'Неверный формат конфиг файла: {e}')

    def _get_template_path(self) -> Path:
        '''Возвращает путь к PDF шаблону из настроек (.env).'''
        # Берем путь из настроек (FILE_STORAGE_TEMPLATE)
        template_path_str = settings.FILE_STORAGE_TEMPLATE

        if not template_path_str:
            raise ValidationException(
                'Не указан путь к PDF шаблону. Установите FILE_STORAGE_TEMPLATE в .env файле'
            )

        template_path = Path(template_path_str)

        if not template_path.exists():
            raise FileNotFoundError(
                f'PDF шаблон не найден: {template_path}. '
                f'Проверьте путь FILE_STORAGE_TEMPLATE в .env файле'
            )

        logger.info(f'Используется PDF шаблон: {template_path}')
        return template_path

    def _format_date(self, date_value: date) -> str:
        '''Форматирует дату в русский формат.'''
        months = {
            1: 'января',
            2: 'февраля',
            3: 'марта',
            4: 'апреля',
            5: 'мая',
            6: 'июня',
            7: 'июля',
            8: 'августа',
            9: 'сентября',
            10: 'октября',
            11: 'ноября',
            12: 'декабря',
        }
        return f'{date_value.day} {months[date_value.month]} {date_value.year} года'

    def _format_datetime(self, datetime_value: datetime | date) -> str:
        '''Форматирует datetime или date в русский формат.'''
        if isinstance(datetime_value, datetime):
            return self._format_date(datetime_value.date())
        elif isinstance(datetime_value, date):
            return self._format_date(datetime_value)
        else:
            return str(datetime_value)

    def _format_number(self, value: float) -> str:
        '''Форматирует число с пробелами и двумя знаками после запятой.'''
        return f'{value:,.2f}'.replace(',', ' ').replace('.', ',')

    def _format_taxable(self, taxable: bool) -> str:
        '''Форматирует булево значение для НДС.'''
        return 'НДС не облагается.' if not taxable else 'НДС облагается.'

    def _prepare_static_data(self, payment_detail: Any) -> Dict[str, str]:
        '''
        Подготавливает статичные данные из PaymentDetail для заполнения.

        Args:
            payment_detail: Сущность PaymentDetail

        Returns:
            Словарь с данными для заполнения статичных полей
        '''
        return {
            'inn': str(payment_detail.inn),
            'kpp': str(payment_detail.kpp) if payment_detail.kpp else '0',
            'index_address': str(payment_detail.index_address),
            'address': str(payment_detail.address),
            'bank_account': str(payment_detail.bank_account),
            'correspondent_account': str(payment_detail.correspondent_account),
            'bik': str(payment_detail.bik),
            'bank_recipient': str(payment_detail.bank_recipient),
        }

    def _prepare_dynamic_data(self, payment: Any) -> Dict[str, str]:
        '''
        Подготавливает динамические данные из ClientPayment для заполнения.

        Args:
            payment: Сущность ClientPayment

        Returns:
            Словарь с данными для заполнения динамических полей
        '''
        data = {
            'name': str(payment.name),
            'paid': self._format_number(payment.paid),
            'paid_str': str(payment.paid_str),
            'pade_date': self._format_date(payment.pade_date),
            'taxable': self._format_taxable(payment.taxable),
        }

        if payment.paid_deadline:
            # Обрабатываем как date, так и datetime
            if isinstance(payment.paid_deadline, datetime):
                data['paid_deadline'] = self._format_date(payment.paid_deadline.date())
            elif isinstance(payment.paid_deadline, date):
                data['paid_deadline'] = self._format_date(payment.paid_deadline)
            else:
                data['paid_deadline'] = str(payment.paid_deadline)
        else:
            data['paid_deadline'] = ''

        if payment.condition:
            data['condition'] = str(payment.condition)
        else:
            data['condition'] = ''

        return data

    def _create_overlay_pdf(
        self, data: Dict[str, str], fields_config: Dict[str, Any]
    ) -> BytesIO:
        '''
        Создает PDF с текстом для наложения на шаблон.

        Args:
            data: Словарь с данными для заполнения
            fields_config: Конфигурация полей из JSON

        Returns:
            BytesIO объект с PDF
        '''
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        # PDF координаты: (0,0) внизу слева, Y растет вверх
        page_height = A4[1]  # Высота страницы A4 в точках

        for field_name, field_value in data.items():
            if field_name not in fields_config:
                continue

            field_config = fields_config[field_name]
            x = field_config['x']
            y = page_height - field_config['y']  # Инвертируем Y координату

            font_name = field_config.get('font_name', 'Helvetica')
            font_size = field_config.get('font_size', 10)
            align = field_config.get('align', 'left')

            # Устанавливаем шрифт
            c.setFont(font_name, font_size)

            # Выравнивание текста
            if align == 'right':
                text_width = c.stringWidth(str(field_value), font_name, font_size)
                x = x - text_width
            elif align == 'center':
                text_width = c.stringWidth(str(field_value), font_name, font_size)
                x = x - (text_width / 2)

            # Рисуем текст
            c.drawString(x, y, str(field_value))

        c.save()
        buffer.seek(0)
        return buffer

    def fill_invoice_template(self, payment: Any, payment_detail: Any) -> bytes:
        '''
        Заполняет PDF шаблон счета данными из payment и payment_detail.

        Args:
            payment: Сущность ClientPayment
            payment_detail: Сущность PaymentDetail

        Returns:
            bytes: Готовый PDF документ в виде байтов
        '''
        try:
            # Загружаем шаблон
            template_path = self._get_template_path()
            template_reader = PdfReader(str(template_path))
            template_writer = PdfWriter()

            # Копируем страницы шаблона
            for page in template_reader.pages:
                template_writer.add_page(page)

            # Подготавливаем данные
            static_data = self._prepare_static_data(payment_detail)
            dynamic_data = self._prepare_dynamic_data(payment)

            # Объединяем все данные
            all_data = {**static_data, **dynamic_data}
            all_fields_config = {
                **self.config['fields']['static'],
                **self.config['fields']['dynamic'],
            }

            # Создаем overlay PDF с текстом
            overlay_buffer = self._create_overlay_pdf(all_data, all_fields_config)
            overlay_reader = PdfReader(overlay_buffer)

            # Накладываем overlay на первую страницу шаблона
            template_page = template_writer.pages[0]
            overlay_page = overlay_reader.pages[0]
            template_page.merge_page(overlay_page)

            # Сохраняем результат в bytes
            output_buffer = BytesIO()
            template_writer.write(output_buffer)
            output_buffer.seek(0)

            result = output_buffer.read()
            logger.info(
                f'PDF документ успешно сгенерирован для платежа ID={payment.id}'
            )
            return result

        except Exception as e:
            logger.error(f'Ошибка при генерации PDF: {e}')
            raise Exception(f'Ошибка при генерации PDF документа: {e}')
