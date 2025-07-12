FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY cloud_server.py .

EXPOSE 8080

CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 cloud_server:app 