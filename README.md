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


# Как установить и запустить бота? (Docker и docker-compose)

> Все найстроки будут проведены на системе Linux с пользователя без прав **root**. Для развёртывания рекомендуется проводить найстроки и установку, cоздав учетную запись без прав root.

Прежде всего необходимо обновить действующий список пакетов: `sudo apt update`

Затем установите несколько обязательных пакетов, которые позволяют aptиспользовать пакеты через HTTPS:  

`sudo apt install apt-transport-https ca-certificates curl software-properties-common`

Затем добавьте в свою систему ключ GPG для официального репозитория Docker:

`curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`

Добавьте репозиторий Docker в источники APT:

`sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"`

- [x] **Установим Docker:**

`sudo apt install docker-ce`

Для установки docker-compose пропишите следующую команду: `pip install docker-compose`

Теперь для того, чтобы начать развёртывать приложение необходимо будет создать директорию `mkdir tg_bot` и переходим в неё 

`cd && cd tg_bot`

После прописываем следущую команду, чтобы скопировать репозиторий github:

`git clone https://github.com/h0riz4n/lottery_bot`

 - **Теперь переходим к развёртыванию нашего приложения.**
 
 Прежде всего Вам будет необходимо изменить файл ./nginx-conf/nginx.conf на [эту конфигурацию]()
