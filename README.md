# [Тelegiv telegram bot](https://github.com/h0riz4n/lottery_bot)
![Иллюстрация к проекту](https://github.com/h0riz4n/lottery_bot/blob/main/picture.png)
> Телеграм бот для проведения лотереи среди пользователей в телеграме.

# Технологии разработки
- Python 3.10.4
- Aiogram (фреймворк для разработки бота)
- Asyncpg (библиотека для работы с базой данных)
- Apscheduler (библиотека для переодических задач)
- PostgreSQL (СУБД)
- Docker and docker-compose (ПО для контейнеризации)
- Nginx (прокси-сервер)
- Let's Encrypt (центр сертификации)

# Как установить и запустить бота?

> Все найстроки будут проведены на системе Linux с суперпользователя **root**. Для развёртывания рекомендуется проводить найстроки и установку, cоздав учетную запись без прав root.

Прежде всего необходимо обновить действующий список пакетов ```sudo apt update```

Затем установите несколько обязательных пакетов, которые позволяют aptиспользовать пакеты через HTTPS:
```sudo apt install apt-transport-https ca-certificates curl software-properties-common```
