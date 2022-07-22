# [Тelegiv telegram bot](https://github.com/h0riz4n/lottery_bot)
![Иллюстрация к проекту](https://github.com/h0riz4n/lottery_bot/blob/main/telegib_vot.jpg)
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

 ## Теперь переходим к развёртыванию нашего приложения.
 
Прежде всего Вам будет необходимо изменить файл `./nginx-conf/nginx.conf` на [эту конфигурацию](https://github.com/h0riz4n/lottery_bot/blob/main/nginx-conf/nginx_2.conf) и в volumes сервиса webserver файла docker-compose.yml провести следующие изменения:
- Небходимо будет добавить `- ./nginx-conf:/etc/nginx/conf.d` и убрать или закомментировать строку `- ./nginx-conf/nginx.conf:/etc/nginx/nginx.conf`

Потом, **находясь в директории с файлом docker-compose.yml,** прописываем команду: `docker-compose up -d` _(флаг **-d** необходим, чтобы запустить развёртывание в фоновом режиме)_

После успешного запуска заходим снова в файл `./nginx-conf/nginx.conf` и вводим [данную конфигурацию](https://github.com/h0riz4n/lottery_bot/blob/main/nginx-conf/nginx.conf)

### В папке nginx-conf должен всегда находиться один файл nginx.conf. Все изменения введутся только в одном файле.

После того как мы ввели [новую конфигурацию](https://github.com/h0riz4n/lottery_bot/blob/main/nginx-conf/nginx.conf) для `nginx.conf` и необходимо убедиться, что в файле `./config/webhook_cfg.py` стоят [теже параметры](https://github.com/h0riz4n/lottery_bot/blob/main/config/webhook_cfg.py)

_Так же в файле nginx.conf прошу обращать внимание на **/** в строке proxy_pass._

Для запуска бота прописываем команду:`docker-compose build && docker-compose up -d`

### И телеграм бот теперь запущен и готов к работе!
