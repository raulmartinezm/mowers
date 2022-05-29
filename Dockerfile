FROM python:3.10.4
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1
# Install and setup poetry
RUN pip install -U pip \
    && pip install black nox \
    && apt-get update \
    && apt install -y curl netcat \
    && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"

RUN mkdir -p /mowers-challenge

COPY src/ /mowers-challenge/src/
COPY tests/ /mowers-challenge/tests/
COPY pyproject.toml /mowers-challenge/
COPY poetry.lock /mowers-challenge/
COPY noxfile.py /mowers-challenge/
COPY .flake8 /mowers-challenge/
COPY README.rst /mowers-challenge/
COPY .darglint /mowers-challenge/
COPY docs/ /mowers-challenge/docs/

WORKDIR /mowers-challenge

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

#CMD nox
CMD poetry run pytest
