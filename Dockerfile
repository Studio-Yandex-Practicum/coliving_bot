FROM python:3.12-slim as requirements

WORKDIR ./app
COPY requirements/prod.txt .
RUN mv prod.txt requirements.txt
RUN pip install --upgrade pip

FROM python:3.12-slim as base

COPY --from=requirements ./app ./app

WORKDIR ./app
RUN pip install -r ./requirements.txt --no-cache-dir

COPY ./src ./