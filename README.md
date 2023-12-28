# Telegram-Бот Коливингов

# Описание проекта

## Используемый стек

[![Python][Python-badge]][Python-url]
[![Django][Django-badge]][Django-url]
[![DRF][DRF-badge]][DRF-url]
[![Python-telegram-bot][Python-telegram-bot-badge]][Python-telegram-bot-url]
[![Postgres][Postgres-badge]][Postgres-url]
[![Nginx][Nginx-badge]][Nginx-url]

## Архитектура проекта

| Директория    | Описание                                                |
|---------------|---------------------------------------------------------|
| `infra`       | Файлы для запуска с помощью Docker, настройки Nginx     |
| `src/backend` | Код Django приложения                                   |
| `src/bot`     | Код бота                                                |

# Подготовка

## Требования

1. **Python 3.12**  
   Убедитесь, что у вас установлена нужная версия Python или активирована в
   pyenv.

2. **Poetry**  
   Зависимости и пакеты управляются через poetry. Убедитесь, что
   poetry [установлен](https://python-poetry.org/docs/#installing-with-the-official-installer)
   на вашем компьютере и ознакомьтесь
   с [документацией](https://python-poetry.org/docs/basic-usage/).  
   Установка зависимостей

```
poetry install
```

Также будет создано виртуальное окружение, если привычнее видеть его в
директории проекта, то
используйте [настройку](https://python-poetry.org/docs/configuration/#adding-or-updating-a-configuration-setting) `virtualenvs.in-project`

3. **Docker**  
   Установите **Docker**.  
   Запуск для **development**:
   Запустите с помощью консоли:
   ```shell
   cd infra/
   docker-compose -f docker-compose.dev.yml up
   ```  
   Также для разработки предусмотрен супер пользователь, но придется
   поменять у него пароль вручную:   
   **Делать нижеперечисленное нужно в новом терминале!**  
   Узнайте ID контейнера *backend*'а, командой:
   ```shell
   docker container ls
   # примерный ответ
   СONTAINER ID  IMAGE  COMMAND  CREATED  STATUS  PORTS  NAMES
   # нам нужно значение из первой колонки
   ```
   Далее используйте команду, чтобы подключиться к терминалу контейнера:
   ```shell
   docker compose -f docker-compose.dev.yml exec -it backend bash
   # должно появится что-то подобное
   root@6449ab29fb81:/app#
   # вводите
   python manage.py changepassword admin
   # и вводите новый пароль -> ваша админка для проверки готова
   ```
   Запуск для **production**:  
   В файле `docker-compose.production.yml` замените `# change to your image`
   на образы с **Docker Hub**.
   Внесите изменения в файл `default.conf`.
   Запустите с помощью консоли:
   ```shell
   cd infra/
   docker-compose -f docker-compose.prod.yml up
   ```

4. **Файлы requirements**  
   Файлы редактировать вручную не нужно. Обновляются через pre-commit хуки (
   если есть изменение в зависимостях, то список обновится при коммите).

5. **pre-commit**  
   [Документация](https://pre-commit.com/)  
   При каждом коммите выполняются хуки (автоматизации) перечисленные в
   .pre-commit-config.yaml. Если не понятно какая ошибка мешает сделать коммит
   можно запустить хуки вручную и посмотреть ошибки:

```shell
pre-commit run --all-files
```

6. **Создание Telegram бота**  
   [Документация](https://core.telegram.org/bots/features#botfather)  
   Перед запуском нужно получить **token** у бота
   [@BotFather](https://t.me/BotFather). После того как бот будет
   зарегестрирован - вам выдадут **token**, его нужно добавить в файл `.env`,
   строку `TOKEN=`. В документе `env.example` она обозначена комментарием.  
   *Про более подробное создание бота читать в приложенной документации.*

## Стиль кода

Придерживаемся [black style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)

## Ветки Git

1. Создавая новую ветку, наследуйтесь от ветки develop, подхватывайте перед
   этим последние изменения
2. Правила именования веток

- весь новый функционал — feature/название-функционала
- исправление ошибок — fix/название-багфикса

3. 1 ветка - 1 задача

# Разворачиваем проект локально

Устанавливаем зависимости

Создаём `.env` файл в корневой директории проекта и заполняем его по
образцу `.env.example`

Переходим в директорию `src/backend/`

```shell
cd src/backend/
```

Применяем миграции

```shell
python manage.py migrate
```

Загружаем фикстуры (локации)

```shell
python manage.py import_locations
```

Запускаем *development*-сервер *Django*

```shell
python manage.py runserver
```

Запускаем бота

Перед выполнением команд откройте новый терминал
(не забываем добавить **token** бота в файл `.env`, строку `TOKEN=`)

```shell
cd src/bot/
python run_bot.py
```

<!-- MARKDOWN LINKS & BADGES -->

[Python-url]: https://www.python.org/

[Python-badge]: https://img.shields.io/badge/Python-376f9f?style=for-the-badge&logo=python&logoColor=white

[Django-url]: https://github.com/django/django

[Django-badge]: https://img.shields.io/badge/Django-0c4b33?style=for-the-badge&logo=django&logoColor=white

[DRF-url]: https://github.com/encode/django-rest-framework

[DRF-badge]: https://img.shields.io/badge/DRF-a30000?style=for-the-badge

[Python-telegram-bot-url]: https://github.com/python-telegram-bot/python-telegram-bot

[Python-telegram-bot-badge]: https://img.shields.io/badge/python--telegram--bot-4b8bbe?style=for-the-badge

[Postgres-url]: https://www.postgresql.org/

[Postgres-badge]: https://img.shields.io/badge/postgres-306189?style=for-the-badge&logo=postgresql&logoColor=white

[Nginx-url]: https://nginx.org

[Nginx-badge]: https://img.shields.io/badge/nginx-009900?style=for-the-badge&logo=nginx&logoColor=white
