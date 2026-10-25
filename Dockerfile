FROM python:3.13-slim

WORKDIR /app

# Changing the source code does not invalidate the dependency install layer.
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

ARG APP_ENV=development
ENV APP_ENV=${APP_ENV} \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY src/ ./src/
COPY test/ ./test/

CMD ["python", "src/app.py"]
