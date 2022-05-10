FROM python:3.9-alpine

WORKDIR /app

# RUN apt-get update && apt-get upgrade -y
RUN apk update
RUN apk add curl gcc musl-dev libffi-dev

RUN curl -sSL https://install.python-poetry.org | python -

ENV PATH /root/.local/bin:$PATH
RUN poetry config virtualenvs.create false

RUN poetry --help # will be successful
ADD pyproject.toml poetry.lock /app/

RUN poetry install

ADD . /app/

ENTRYPOINT ["poetry", "run", "spotify2apple"]