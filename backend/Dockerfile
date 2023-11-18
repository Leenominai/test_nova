FROM python:3.9-slim-buster

RUN pip3 install --upgrade pip && pip3 install poetry

WORKDIR /backend

COPY poetry.lock pyproject.toml entrypoint.sh ./

RUN poetry config virtualenvs.create false && poetry install --without test --no-interaction --no-ansi

COPY docmanager /backend

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

CMD ["gunicorn", "docmanager.wsgi:application", "--bind", "0:8000" ]

LABEL author='leenominai' version='develop v1.0' broken_keyboards=1
