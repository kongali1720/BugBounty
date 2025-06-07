# 1. docker-compose.yml lengkap

version: '3.8'

services:
  bugbounty-app:
    build: .
    ports:
      - "5000:5000"
    environment:
      FLASK_ENV: production
      FLASK_APP: app.py
      MYSQL_HOST: db
      MYSQL_USER: bugbounty
      MYSQL_PASSWORD: secret123
      MYSQL_DB: bugbountydb
    depends_on:
      - db
    volumes:
      - .:/app
    command: flask run --host=0.0.0.0

  db:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: bugbountydb
      MYSQL_USER: bugbounty
      MYSQL_PASSWORD: secret123
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql

volumes:
  mysql-data:
  
# 2. Cara koneksi MySQL di Flask (contoh app.py snippet)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Ambil config dari env

user = os.getenv('MYSQL_USER', 'bugbounty')
password = os.getenv('MYSQL_PASSWORD', 'secret123')
host = os.getenv('MYSQL_HOST', 'db')
db_name = os.getenv('MYSQL_DB', 'bugbountydb')

# Setup connection string SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Contoh model sederhana
class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)

# Inisialisasi DB (jalankan sekali)
@app.before_first_request
def create_tables():
    db.create_all()

# Route contoh
@app.route('/')
def index():
    bugs = Bug.query.all()
    return '<br>'.join([bug.title for bug in bugs]) or "No bugs found!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    
# 3. Cara jalanin

    docker-compose up --build


# 4. Cek MySQL

Port 3306 dari host di-mapping ke container, jadi bisa kamu akses langsung dari luar kalau perlu
Data MySQL tersimpan di mysql-data volume biar persistent
Summary

Pakai Docker Compose supaya gampang start app + DB
Flask terhubung ke MySQL pakai environment variable
Bisa langsung extend buat fitur BugBounty yang butuh database
