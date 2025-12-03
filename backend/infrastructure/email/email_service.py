import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.core.settings import settings
from backend.core.logger import logger
import asyncio
from typing import Optional


class EmailService:
    '''Сервис отправки emails'''

    @staticmethod
    async def send_verification_email(
        email: str, verification_code: str, first_name: str
    ) -> bool:
        '''Отправить код верификации по email'''

        subject = 'Подтвердите вашу почту в Attorney CRM'

        # HTML письмо
        html_content = f'''
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; }}
                    .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
                    .header {{ text-align: center; color: #333; margin-bottom: 20px; }}
                    .code-box {{ 
                        background: #f0f0f0; 
                        border: 2px solid #007bff; 
                        border-radius: 8px; 
                        padding: 20px; 
                        text-align: center; 
                        margin: 20px 0;
                    }}
                    .code {{ font-size: 32px; font-weight: bold; color: #007bff; letter-spacing: 5px; }}
                    .footer {{ text-align: center; color: #999; font-size: 12px; margin-top: 20px; }}
                    .warning {{ color: #d9534f; font-size: 12px; margin-top: 10px; }}
                </style>
            </head>
            <body>
                <div class='container'>
                    <div class='header'>
                        <h1>Добро пожаловать в Attorney CRM! 👨‍⚖️</h1>
                    </div>
                    
                    <p>Привет, {first_name}!</p>
                    <p>Спасибо за регистрацию. Для завершения регистрации подтвердите вашу почту, введя код ниже:</p>
                    
                    <div class='code-box'>
                        <div class='code'>{verification_code}</div>
                    </div>
                    
                    <p>Этот код действителен <strong>15 минут</strong>.</p>
                    <p>Если вы не регистрировались, просто проигнорируйте это письмо.</p>
                    
                    <div class='footer'>
                        <p>&copy; 2025 Attorney CRM. Все права защищены.</p>
                        <p class='warning'>⚠️ Не делитесь этим кодом никому!</p>
                    </div>
                </div>
            </body>
        </html>
        '''

        return await EmailService._send_email(
            to_email=email, subject=subject, html_content=html_content
        )

    @staticmethod
    async def send_password_reset_email(
        email: str, reset_code: str, first_name: str
    ) -> bool:
        '''Отправить код сброса пароля'''

        subject = 'Сброс пароля в Attorney CRM'

        html_content = f'''
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; }}
                    .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 20px; }}
                    .code-box {{ background: #f0f0f0; padding: 20px; text-align: center; border-radius: 8px; }}
                    .code {{ font-size: 28px; font-weight: bold; color: #d9534f; letter-spacing: 3px; }}
                </style>
            </head>
            <body>
                <div class='container'>
                    <h2>Сброс пароля</h2>
                    <p>Привет, {first_name}!</p>
                    <p>Вы запросили сброс пароля. Используйте код ниже:</p>
                    
                    <div class='code-box'>
                        <div class='code'>{reset_code}</div>
                    </div>
                    
                    <p>Код действителен <strong>30 минут</strong>.</p>
                </div>
            </body>
        </html>
        '''

        return await EmailService._send_email(
            to_email=email, subject=subject, html_content=html_content
        )

    @staticmethod
    async def _send_email(to_email: str, subject: str, html_content: str) -> bool:
        '''Отправить email в отдельном потоке (не блокирует приложение)'''

        def send_sync():
            try:
                # Создаём письмо
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = settings.smtp_from
                msg['To'] = to_email

                # Добавляем HTML
                msg.attach(MIMEText(html_content, 'html'))

                # Подключаемся к SMTP серверу
                with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                    server.starttls()  # Включаем шифрование TLS
                    server.login(
                        settings.smtp_user, settings.smtp_password
                    )  # Аутентификация
                    server.send_message(msg)  # Отправка

                logger.info(f'[EMAIL] Письмо отправлено на {to_email}')
                return True

            except Exception as e:
                logger.error(f'[EMAIL] Ошибка отправки письма {to_email}: {e}')
                return False

        # Запустить в отдельном потоке (не блокирует async)
        loop = asyncio.get_event_loop()
        # Запускает синхронный код (send_sync) в отдельном потоке, чтобы не блокировать асинхронный цикл.
        return await loop.run_in_executor(None, send_sync)
