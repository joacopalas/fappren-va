FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data

ENV PORT=8000

EXPOSE 8000

CMD ["sh", "-c", "gunicorn myproject.wsgi:application --bind 0.0.0.0:${PORT} --workers 2"]
