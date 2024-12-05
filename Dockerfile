# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Salin requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Salin folder config, file model, dan semua file aplikasi lainnya
COPY config /app/config/
COPY MoneyDetector.h5 /app/
COPY . /app/

# Ekspos port 8000
EXPOSE 8000

# Jalankan aplikasi
CMD ["python", "app.py"]
