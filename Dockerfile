FROM python:3.10.8-slim

EXPOSE 8000

RUN apt update
RUN apt upgrade -y

COPY . /question-answer-api
WORKDIR /question-answer-api

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn"]

CMD ["-c", "python:config.gunicorn", "src.app:create_app()"]
