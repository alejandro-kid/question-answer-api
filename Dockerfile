FROM python:3.10.8-slim

EXPOSE 8000

RUN apt update
RUN apt upgrade -y
RUN apt install -y wget

COPY . /question-answer-api
WORKDIR /question-answer-api

RUN wget https://gpt4all.io/models/ggml-gpt4all-j-v1.3-groovy.bin
ENV LLMS_MODEL_PATH="/question-answer-api/ggml-gpt4all-j-v1.3-groovy.bin"

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn"]

CMD ["-c", "python:config.gunicorn", "src.app:create_app()"]
