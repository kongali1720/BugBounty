## 🚀 Jalankan dengan Docker

1. Build image

```bash
docker build -t bugbounty-app .
```

---

2. Jalankan container

        docker run -p 5000:5000 bugbounty-app
   
Buka 

        http://localhost:5000 di browser

# Gunakan image python versi slim yang ringan

    FROM python:3.11-slim

# Set working directory di container

    WORKDIR /app

# Copy requirements dulu supaya cache layer bisa dipakai

    COPY requirements.txt .

# Install dependencies

    RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file project ke container

    COPY . .

# Expose port 5000

    EXPOSE 5000

# Environment variable supaya Flask jalan di mode production

    ENV FLASK_ENV=production
    ENV FLASK_APP=app.py

# Jalankan app.py saat container start

    CMD ["flask", "run", "--host=0.0.0.0"]

---

# Penjelasan:

build: .

Bangun image dari Dockerfile di root project

ports: "5000:5000"

Buka port 5000 ke luar container

environment

Set environment variable Flask supaya production dan app.py sebagai entrypoint

volumes

Mount folder lokal ke container, biar bisa update kode langsung tanpa build ulang (bagus buat development)

command

Jalankan Flask server yang listen di semua interface

## Cara pakai:

Jalankan

        docker-compose up --build
        
Buka browser

        http://localhost:5000
        
Stop dengan Ctrl+C
