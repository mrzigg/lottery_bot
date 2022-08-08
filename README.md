# [Тelegiv telegram bot](https://github.com/h0riz4n/lottery_bot)
![Иллюстрация к проекту](https://github.com/h0riz4n/lottery_bot/blob/main/telegiv_bot.jpg)
> Телеграм бот от Telegiv для проведения лотереи среди пользователей в телеграме.

# Технологии разработки
- Python 3.10.4
- Aiogram (фреймворк для разработки бота)
- Asyncpg (библиотека для работы с базой данных)
- Apscheduler (библиотека для переодических задач)
- PostgreSQL (СУБД)
- Docker and docker-compose (ПО для контейнеризации)
- Nginx (прокси-сервер)
- Let's Encrypt (центр сертификации)

# Описание бота.
Бот проводит розыгрыши, данные которых он получает с backend-сервера, и начинает проводить розыгрыши среди пользователей телеграм, которые выполняют условия участия. Бот работает на webhook соединениях. Для реализации и запуска бота, будут необходимы домены, которые будут корректно зарегистрированы по IP VPS сервера. Технологии разработки, которые применялись, указаны выше. Во время проведения розыгрыша бот выдаёт билеты за различные бонусы, а также за каждого приглашённого друга по реферальной ссылке будут выдаваться дополнительные бонусы. По окончанию розыгрыша бот по случайному билету выбирает победителя(-победителей) и уведомляет всех участников розыгрыша о его результатах. С каждым накопленным билетом увеличивается возможность победить.

> Прежде чем запустить бота, необходимо провести настройку конфигурации в файле variables.py и задать правильные параметры, а также в /config/webhook_cfg.py. Лучше переменные будут заданы через переменные окружения.

# Как установить и запустить бота? (Docker и docker-compose)

> Все найстроки будут проведены на системе Linux с пользователя без прав **root**. Для развёртывания рекомендуется проводить найстроки и установку, cоздав учетную запись без прав root.

Прежде всего необходимо обновить действующий список пакетов: `sudo apt update`

Затем установите несколько обязательных пакетов, которые позволяют apt использовать пакеты через HTTPS:  

`sudo apt install apt-transport-https ca-certificates curl software-properties-common`

Затем добавьте в свою систему ключ GPG для официального репозитория Docker:

`curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`

Добавьте репозиторий Docker в источники APT:

`sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"`

Затем снова обновите действующий список пакетов: `sudo apt update`

- [x] **Установим Docker:**

`sudo apt install docker-ce`

Для установки docker-compose пропишите следующие команды: `sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`

`sudo chmod +x /usr/local/bin/docker-compose`

Теперь для того, чтобы начать развёртывать приложение необходимо будет создать директорию `mkdir telegram_bot` и переходим в неё `cd && cd telegram_bot`

После прописываем следущую команду, чтобы скопировать репозиторий github:

`git clone https://github.com/h0riz4n/lottery_bot`

> Либо же можете установить FileZilla, ввести в неё все необходимые данные сервера: ip-адрес, логин (root), пароль, порт (22) и через приложение вручную перенести файлы на сервер в директорию telegram_bot.

И в директории telegram_bot создаём директории: `mkdir views && mkdir dhparam`

 ## Теперь переходим к развёртыванию нашего приложения.
 
Прежде всего Вам будет необходимо изменить файл `./nginx-conf/nginx.conf` на [эту конфигурацию](https://github.com/h0riz4n/lottery_bot/blob/main/nginx-conf/nginx_2.conf) _(не забудьте изменить в **8** строке example.com на **имя вашего домена**)_ и в volumes сервиса webserver файла docker-compose.yml провести следующие изменения:
- Небходимо будет добавить `- ./nginx-conf:/etc/nginx/conf.d` и убрать или закомментировать строку `- ./nginx-conf/nginx.conf:/etc/nginx/nginx.conf`

Потом, **находясь в директории с файлом docker-compose.yml,** прописываем команду: `docker-compose up -d` _(флаг **-d** необходим, чтобы запустить развёртывание в фоновом режиме)_ 

После успешного запуска прописываем `docker-compose down` и заходим снова в файл `./nginx-conf/nginx.conf` и вводим [данную конфигурацию](https://github.com/h0riz4n/lottery_bot/blob/main/nginx-conf/nginx.conf)

### В папке nginx-conf должен всегда находиться один файл nginx.conf. Все изменения введутся только в одном файле.

После того как мы ввели [новую конфигурацию](https://github.com/h0riz4n/lottery_bot/blob/main/nginx-conf/nginx.conf) для `nginx.conf` _(не забудьте изменить в **9**, **31** и **32** example.com на **имя вашего домена**)_ и необходимо убедиться, что в файле `./config/webhook_cfg.py` стоят [те же параметры](https://github.com/h0riz4n/lottery_bot/blob/main/config/webhook_cfg.py), а именно:

- WEBHOOK_HOST - имя вашего домена;
- WEBHOOK_PATH - имя директории, в которой находится бот (в данном случае telegram_bot)
- Остальные данные без изменений

> Также в файле nginx.conf прошу обращать внимание на **/** в строке proxy_pass. Если всё запустилось успешно, но бот не реагирует на сообщения, попробуйте убрать или добавить **/** в конце строки: `proxy_pass http://telegram_bot:3001/;`

Также пропишите команду, указав правильно директорию: `sudo openssl dhparam -out /root/**telegram_bot**/dhparam/dhparam-2048.pem 2048`

Это необходимо для создания ключа Diffie-Hellman и прямой секретности.

Для запуска бота прописываем команду:`docker-compose build && docker-compose up -d`

### И телеграм бот теперь запущен и готов к работе!

# Запуск бота на Localhost. (Nginx и Let's Encrypt)

Прежде всего необходимо обновить действующий список пакетов: `sudo apt update`

После прописываем следущую команду, чтобы скопировать репозиторий github:

`git clone https://github.com/h0riz4n/lottery_bot`

> Либо же можете установить FileZilla, ввести в неё все необходимые данные сервера: ip-адрес, логин (root), пароль, порт (22) и через приложение вручную перенести файлы на сервер.

Далее необходимо установить **nginx**: `sudo apt install nginx`

- Для того, чтобы проверить успешно ли прошла установка, можно прописать следующую команду: `sudo ufw app list`
> Вывод должен быть следующим:

![image](https://user-images.githubusercontent.com/100841904/183039107-b6e6e757-8ab0-462c-b31d-dc45de116d93.png)

Далее необходимо будет открыть **80 порт**: `sudo ufw allow 'Nginx HTTP'`

Перезапускаем **ufw**: `sudo ufw enable`

- Для того, чтобы проверить успешно ли прошла установка, можно прописать следующую команду: `sudo ufw status`
> Вывод должен быть следующим:

![image](https://user-images.githubusercontent.com/100841904/183040055-050fff1e-a5a1-4d87-8b64-86889f28e65b.png)

- Также проверим статус **nginx**: `systemctl status nginx`
> Должно вывести следующее:

![image](https://user-images.githubusercontent.com/100841904/183040428-0011c696-4698-4137-9e6c-94c2fc88c24b.png)

> **Не забываем везде изменять your_domain на имя вашего домена**

Далее создадим каталог для your_domain, используя **-p** флаг для создания любых необходимых родительских каталогов: `sudo mkdir -p /var/www/your_domain/html`

Затем назначаем право собственности на каталог с $USER помощью переменной среды: `sudo chown -R $USER:$USER /var/www/your_domain/html`   

- Проверим необходимые разрешения: `sudo chmod -R 755 /var/www/your_domain` 

Создадим образец _index.html_: `sudo nano /var/www/your_domain/html/index.html`

Внутри добавляем [следующее](https://github.com/h0riz4n/lottery_bot/blob/main/index.html)

Открываем конфигурацию нашего сервера: `sudo nano /etc/nginx/sites-available/your_domain` 

И прописываем в нем [данную конфигурацию](https://github.com/h0riz4n/lottery_bot/blob/main/nginx-conf/nginx_4.conf)

Далее включим файл, создав из него ссылку на sites-enabled каталог: `sudo ln -s /etc/nginx/sites-available/your_domain /etc/nginx/sites-enabled/`

Далее в файле `/etc/nginx/nginx.conf` убираем комментарий со строки: `server_names_hash_bucket_size 64;`

- Проверяем, что ошибок нет: `sudo nginx -t`

И перезапускаем **nginx**: `sudo systemctl restart nginx`

## Работаем с let's encrypt:

В начале устанавливаем certbot: `sudo apt install certbot python3-certbot-nginx`

Разрешаем трафик **HTTPS**: `sudo ufw allow 'Nginx Full'`

`sudo ufw delete allow 'Nginx HTTP'`

Разрешаем серверу прослушивать **80** и **443** порты: 
- `sudo ufw allow http`
- `sudo ufw allow 80`
- `sudo ufw allow https`
- `sudo ufw allow 443`

Получаем сертификаты (вместо example.com указываем **имя домена**): `sudo certbot --nginx -d example.com -d www.example.com` 

> Certbot запросит у вас адрес эл. почты (можно указать любой), принять условия обслуживания и предпочитаемый вариант настройки. Выбираем предпочитаемый вариант и, при успешной установке, вывод должен быть следующим:

![image](https://user-images.githubusercontent.com/100841904/183045729-875ed73b-a546-4e67-9e1e-acde6a07d496.png)

Далее открываем **nginx.conf** в каталоге `/etc/nginx`: `sudo nano /etc/nginx/nginx.conf`

Внутри вводим [данную конфигурацию](https://github.com/h0riz4n/lottery_bot/blob/main/nginx-conf/nginx_3.conf) и необходимо убедиться, что в файле `./config/webhook_cfg.py` стоят [нужные параметры](https://github.com/h0riz4n/lottery_bot/blob/main/config/webhook_cfg.py), а именно:
- WEBHOOK_HOST - имя вашего домена
- WEBHOOK_PATH - рабочая директория (/telegram_bot/)
- WEBAPP_HOST - ip-адрес (127.0.0.1)
- WEBAPP_PORT - порт (3001)

Далее необходимо установить все необходимые [библиотеки](https://github.com/h0riz4n/lottery_bot/blob/main/requirements.txt)
- `sudo apt-get install python3-pip`
-  `pip install aiogram`
-  `pip install asyncpg`
-  `pip install apscheduler`

Создаём сервис бота: `cd ../ && cd etc/systemd/system && nano bot.service`

Внутри прописываем [данную конфигурацию](https://github.com/h0riz4n/lottery_bot/blob/main/bot.service)

> Обращайте внимание на директории и названия файлов (должны совпадать с вашим расположением файлов)

Далее запускаем бота: `systemctl enable bot`

`systemctl start bot`

> Бот расчитан на то, что база данных будет находиться удалённо от бота, поэтому образы **PostgreSQL** не были добавлены в файл `docker-compose.yml`
