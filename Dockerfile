FROM python:3.11-slim

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt

COPY ./*.py /app/
COPY ./*.xlsx /app/

ENTRYPOINT ["python", "Bot.py"]