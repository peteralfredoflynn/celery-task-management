FROM python:3.8-slim

RUN apt-get update \
    && pip install pipenv

ADD . /code
WORKDIR /code

RUN pipenv install --system --deploy
CMD ["gunicorn", "app.application:create_flask_app()", "--workers", "1", "--log-level", "debug", "--bind", "0.0.0.0:5000"]
