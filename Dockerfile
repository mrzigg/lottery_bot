FROM python:3.10.4

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app/

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

RUN cd /usr/src/app

ENV API_TOKEN=""

EXPOSE 3001

ENTRYPOINT ["python3", "app.py"]
