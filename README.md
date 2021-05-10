Telegram бот для учёта расходов. Все расходы разделены на 25 категорий и 5 надкатегорий.
Modified and extended version of original bot: https://github.com/alexey-goloburdin/telegram-finance-bot


В переменные окружения надо добавить API токен бота и ID юзера.

'TELEGRAM_API_TOKEN_PB' — API токен бота

'TELEGRAM_ACCESS_USER_ID' — ID Telegram аккаунта, от которого будут приниматься сообщения (сообщения от остальных аккаунтов игнорируются)

Переменные  окружения необходимые для работы базы данных.

'DB_POSTGRES_TB_NAME' - название базы данных

'DB_POSTGRES_USER' - логин юзера для подключения к базе данных

'DB_POSTGRES_USER_PASSWORD' - пароль юзера

'DB_POSTGRES_HOST' - адрес хоста базы данных (по умолчанию для локального сервера - 127.0.0.1)

'DB_POSTGRES_PORT' - порт хоста базы данных (по умолчанию для локального сервера - 5432)


Roadmap:
    Add statistics.
    Add budget limits.
    Add input expenses with Telegram custom keyboard buttons.
