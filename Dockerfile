FROM python:3.10.4

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app/

RUN pip install aiogram \
    && pip install asyncpg \
    && pip install apscheduler

RUN cd /usr/src/app

ENTRYPOINT ["python3", "app.py"]