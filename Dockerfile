FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

# Use Gunicorn for production; binds to container port 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers", "3"]
