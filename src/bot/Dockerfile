FROM python:3.12-slim

WORKDIR ./app
COPY ../../requirements/prod.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt --no-cache-dir

COPY /src/bot/ .