import logging

logger = logging.getLogger('Bloom')
logger.setLevel(logging.DEBUG)

# Консольный обработчик
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
)

# Файловый обработчик
file_handler = logging.FileHandler('app.log', encoding='utf-8')
# ПОТОМ ВЫВЕСТИ В INFO
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
)

# Добавление обработчиков
logger.addHandler(console_handler)
logger.addHandler(file_handler)
