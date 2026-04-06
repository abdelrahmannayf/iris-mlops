# Stage 1: Builder
FROM python:3.11 AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production
FROM python:3.11-slim
WORKDIR /app

# بنجيب الـ libraries من الـ builder
COPY --from=builder /usr/local/lib/python3.11/site-packages \
     /usr/local/lib/python3.11/site-packages

# بنكوبي الكود
COPY train.py .

# لا تشغل بـ root
RUN useradd -m trainer && chown -R trainer /app
USER trainer

CMD ["python", "train.py"]
