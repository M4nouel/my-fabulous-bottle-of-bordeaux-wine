FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./requirements.txt /app/

RUN apt-get update && \
    apt-get install -y netcat && \
    pip install -r requirements.txt