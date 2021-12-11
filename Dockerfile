FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get upgrade -y

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -

ENV PATH /root/.local/bin:$PATH
RUN poetry config virtualenvs.create false

# RUN poetry --help # will be successful
ADD pyproject.toml poetry.lock /app/

RUN poetry install

ADD . /app/

CMD ["poetry", "run", "spotify2apple"]