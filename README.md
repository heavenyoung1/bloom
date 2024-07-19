## Personal website built with Python, FastAPI (Персональный веб-сайт на Python и FastAPI)

🚨 (ENG) This project is thanks to [Brittany Chiang](https://github.com/bchiang7/v4), by the way this is the fourth version of her project. Brittany's project is written with JavaScript framework - Gatsby, my website is written in FastAPI. You can find all the color schemes and fonts from her link. There are a lot of bugs in this project which will be solved later, now I encourage you to write tickets and make Forks to bring the project to a better level.
If you have any questions, I encourage you to write to [me](https://t.me/heavenyoung) in Telegram.
A more detailed description is at the bottom of the project, I encourage you to familiarize yourself with it. Good luck to everyone!

🚨 (RUS) Этот проект состоялся благодаря [Brittany Chiang](https://github.com/bchiang7/v4), к слову это четвертая версия её проекта. Проект Бриттани написан при помощи фреймворка JavaScript - Gatsby, мой веб-сайт написан на FastAPI. Вcе цветовые решения и шрифты вы можете найти у неё по ссылке. В данном проекте множество недоделок, которые в последующем будут решаться, сейчас же призываю Вас писать тикеты и делать Форки, чтобы довести проект до более качественного уровня.
Новичку, который хочет учить FastAPI, советую познакомиться с видео-уроками [Сурена Хореняна](https://www.youtube.com/watch?v=z4pbneT6SLw&list=PLYnH8mpFQ4akzzS1D9IHkMuXacb-bD4Cl&index=1)
Если у Вас есть какие-либо вопросы, призываю писать [мне](https://t.me/heavenyoung) в Telegram.
Более детальное описание находится внизу проекта, призываю ознакомиться с ним. Всем удачи!

## Внешний Вид
<picture>
  <img alt="Главное меню" src="/screens/1.png">
</picture>

## Установка завимостей

Для запуска этого приложения вам понадобится последняя версия Python.
Чтобы установить зависимости проекта:

```
pip install -r requirements.txt
```
Рекомендую вам работать в виртуальном окружении, чтобы изолировать зависимости от других проектов.

## Запуск приложения

```
uvicorn app.main:app --reload
```

Затем открой браузер на [`http://127.0.0.1:8000`](http://127.0.0.1:8000), чтобы загрузить приложение.

## Изучение документации

Чтобы ознакомиться с документацией по API:

* [`/docs`](http://127.0.0.1:8000/docs) for classic OpenAPI docs

Документация к [тестам Unitest](https://docs.python.org/3/library/unittest.html)


## TODO list

- [ ] Написать тесты Unittest
- [ ] Изолировать эндпоинты, чтобы соблюдать принципы [SOLID](https://habr.com/ru/companies/vk/articles/412699/), а именно Принцип единственной ответственности
- [ ] Автоматизировать тестирование

## Дерево проекта

## Корневая директория
- `alembic/`
  - `versions/`
  - `env.py`
  - `README`
  - `script.py.mako`
- `app/`
  - `__pycache__/`
    - `__init__.cpython-312.pyc`
    - `crud.cpython-312.pyc`
    - `database.cpython-312.pyc`
    - `models.cpython-312.pyc`
    - `schemas.cpython-312.pyc`
  - `__init__.py`
  - `crud.py`
  - `database.py`
  - `models.py`
  - `schemas.py`
- `static/`
  - `__pycache__/`
  - `fonts/`
  - `icons/`
  - `image/`
  - `scripts.js`
  - `style.css`
  - `text.py`
- `templates/`
  - `about.html`
  - `index.html`
  - `navbar.html`
  - `project-item.html`
  - `skills.html`
- `tests/`
  - `test_crud.py`
  - `test_main.py`
- `venv/`
- `.gitignore`
- `alembic.ini`
- `main.py`
- `README.md`
- `requirements.txt`
- `sql_app.db`

## Описание директорий и файлов

- `alembic/`: Каталог для управления миграциями базы данных.
  - `versions/`: Поддиректория для хранения версий миграций.
  - `env.py`: Настройки окружения Alembic.
  - `README`: Документация Alembic.
  - `script.py.mako`: Шаблон скриптов миграции.

- `app/`: Основное приложение.
  - `__init__.py`: Инициализация пакета.
  - `crud.py`: Функции для выполнения CRUD операций.
  - `database.py`: Настройки подключения к базе данных.
  - `models.py`: Определение моделей базы данных.
  - `schemas.py`: Схемы данных для валидации и сериализации.

- `static/`: Статические файлы (CSS, JS, изображения и т.д.).
  - `fonts/`: Шрифты.
  - `icons/`: Иконки.
  - `image/`: Изображения.
  - `scripts.js`: Основной скрипт JavaScript.
  - `style.css`: Основной файл стилей CSS.
  - `text.py`: Файл с элементами данных python

- `templates/`: HTML шаблоны.
  - `about.html`: Страница "Обо мне".
  - `index.html`: Главная страница.
  - `navbar.html`: Шаблон навигационной панели.
  - `project-item.html`: Шаблон элемента проекта.
  - `skills.html`: Страница с навыками.

- `tests/`: Тесты.
  - `test_main.py` 
  - `test_crud.py`

- `venv/`: Виртуальное окружение Python.

- `.gitignore`: Файл для исключения файлов и директорий из системы контроля версий Git.

- `alembic.ini`: Конфигурационный файл Alembic.

- `main.py`: Основной файл запуска приложения.

- `README.md`: Документация проекта.

- `requirements.txt`: Список зависимостей Python.

- `sql_app.db`: База данных SQLite.

## Прочти меня

Этот пет-проект состоялся благодаря [Brittany Chiang](https://github.com/bchiang7/v4). Интерфейс, и то что умёёт её веб-сайт побудили меня взяться сделать то же самое, но при помощи FastAPI. Проект Бриттани написан при помощи фреймворка JavaScript - Gatsby. ВСе цветовые решения и шрифты вы можете найти у неё по ссылке. Веб-сайт Бриттани умеет гораздо больше, чем мой веб-сайт, в моих планах его доработать, так как это моё первое знакомство с FastAPI. Новичку, который хочет познакомиться с FastAPI советую начать с базового изучения документации, а так же видео-уроков [Сурена Хореняна](https://www.youtube.com/watch?v=z4pbneT6SLw&list=PLYnH8mpFQ4akzzS1D9IHkMuXacb-bD4Cl&index=1). 
В данном проекте я изучил и применил на практике конечно же FastAPI, Pydantic, при помощи которого удобно валидировать типы данных, собственно говоря, это является фишкой FastAPI. Шаблоны Jinja показались мне сильно урезанными в функционале, захотелось доработать их, потому что, у меня не получилось сделать то, что я хотел, например вывести результат обычной функции в шаблоне. В данном проекте реализованы схемы Pydantic, модели, которые писал при помощи движка SQLAlchemy. Я, мягко говоря, задался вопросом, зачем использовать Mapped, если можно его не использовать, поэтому большая часть моделей не включает в себя Mapped, а одна включает. База Данных реализована при помощи SQLite, до этого я пользовался PostgreSQL, и мне понравилось то, что здесь не нужен отдельный клиент, связь, логины и пароли и тому подобное. Достаточно просто прописать ссылку на файлик с SQL, где будут храниться наши данные и таблицы. Познакомился со Startlette и то как круто пишется документация при помощи OpenAPI
Один из багов, которые сейчас существуют это извлечение данных из БД при нажатии на Компанию. При нажатии на область Компании происходит вытягивание данных при помощи CRUD - запроса и эти данные, например ID помещаются в запрос после ? в адресной строке. Если у вас есть какие-то вопросы создавайте тикеты к данному проекту или делайте PULL Request. Подобных сайтов-портфолио на Питоне, а именно на FastAPI я не нашёл. Всем удачи. Для связи, пишите [мне](https://t.me/heavenyoung) в Telegram.