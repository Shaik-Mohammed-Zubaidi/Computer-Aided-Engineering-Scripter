# ───────── Build stage ─────────
FROM python:3.11-slim AS builder
WORKDIR /app

# Prevents Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY backend/requirements.txt .
RUN pip install --upgrade pip \
 && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# ───────── Runtime stage ─────────
FROM python:3.11-slim
WORKDIR /app

# Copy wheels and install
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copy application code
COPY backend/ .

# OpenAI key passed at runtime:  -e OPENAI_API_KEY=sk-***
ENV FLASK_ENV=production \
    PYTHONUNBUFFERED=1

EXPOSE 5000
# Gunicorn (async workers handle CORS pre-flight nicely)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
