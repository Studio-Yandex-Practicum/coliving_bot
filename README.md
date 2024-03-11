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
   `pyenv`.

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

4. **Токен Telegram бота**  
   [Документация](https://core.telegram.org/bots/features#botfather)  
   Перед запуском нужно получить **token** у бота
   [@BotFather](https://t.me/BotFather). После того как бот будет
   зарегистрирован - вам выдадут **token**, его нужно добавить в файл `.env`,
   строку `TOKEN=`. В документе `env.example` она обозначена комментарием.  
   *Про более подробное создание бота читать в приложенной документации.*

5. **Файлы requirements**  
   Файлы редактировать вручную не нужно. Обновляются через pre-commit хуки (если есть изменение в зависимостях, то список обновится при коммите).

6. **pre-commit**  
   [Документация](https://pre-commit.com/)  
   Обязательно выполните команду:
   ```shell
   pre-commit install
   ```
   При каждом коммите будут выполняться хуки (автоматизации) перечисленные в
   `.pre-commit-config.yaml`. Если не понятно какая ошибка мешает сделать коммит
   можно запустить хуки вручную и посмотреть ошибки:

   ```shell
   pre-commit run --all-files
   ```
## Стиль кода

Придерживаемся [black style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)

## Ветки Git

1. Создавая новую ветку, наследуйтесь от ветки develop, подхватывайте перед
   этим последние изменения
2. Правила именования веток

   - весь новый функционал — feature/название-функционала
   - исправление ошибок — fix/название-багфикса  
   Пример:
   ```
   feature/burger-menu
   fix/bun-issue
   ```

3. 1 ветка - 1 задача

# Разворачиваем проект в контейнерах
1. Создаём `.env` файл в корневой директории проекта и заполняем его по
образцу `.env.example`

2. Переходим в директорию `infra/`
   ```shell
   cd infra/
   ```

3. Поднимаем контейнеры
   ```shell
   docker compose --env-file ../.env -f docker-compose.local.yml up -d
   ```

4. При первом запуске можно создать записи в БД о городах командой
   ```shell
   docker exec backend python manage.py import_locations
   ```

## Администрирование развёрнутого приложения
### Создание суперпользователя
Используйте команду ниже и следуйте инструкциям в терминале
```shell
docker exec -it backend python manage.py createsuperuser
```

# Разворачиваем проект локально

1. Устанавливаем зависимости

2. Создаём `.env` файл в корневой директории проекта и заполняем его по
образцу `.env.example`

3. Переходим в директорию `src/backend/`
   ```shell
   cd src/backend/
   ```

4. Применяем миграции
   ```shell
   python manage.py migrate
   ```

5. Загружаем фикстуры (локации)
   ```shell
   python manage.py import_locations
   ```

6. Запускаем *development*-сервер *Django*
   ```shell
   python manage.py runserver
   ```

> **Note**  
> Есть возможность изменить используемый файл настроек, определив переменную `DJANGO_SETTINGS_MODULE`,
> например,
> ```shell
> export DJANGO_SETTINGS_MODULE=coliving_bot.settings.stage
> ```

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
