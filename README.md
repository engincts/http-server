# 🖥️ Basit HTTP Sunucusu (Socket + Docker)

Bu proje, framework kullanmadan tamamen Python socket programlama ile yazılmış bir HTTP sunucusudur. Hem temel HTTP isteklerini işler hem de gelişmiş özellikler (routing, POST desteği, threading, vs.) içerir. Ayrıca Docker ve Docker Compose desteğiyle containerize edilmiştir.

---

## 🚀 Özellikler

✅ `GET` ve `POST` isteklerini işler  
✅ `/static/` dizininden dosya sunar  
✅ JSON endpoint: `/api/hello` ve `/api/echo`  
✅ Çoklu bağlantı desteği (threading ile)  
✅ MIME type yönetimi (`Content-Type`)  
✅ 404, 405, 500 hata yanıtları  
✅ Route handler sistemi (`@route`)  
✅ Basit template engine desteği  
✅ Dockerfile ve compose.yaml ile container desteği  
✅ Açık kaynak lisans ve katkı dosyalarıyla uyumlu

---

## 📁 Proje Yapısı
http-server/
├── server.py
├── Dockerfile
├── .dockerignore
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── NOTICE.md
├── CODE_OF_CONDUCT.md
├── compose.yaml
├── static/
└── routes/


---

## 🔧 Çalıştırma (Python)

```bash
python server.py


🐳 Docker ile Çalıştırma

docker build -t http-server .
docker run -p 8080:8080 http-server

📦 Docker Compose ile
docker compose up --build
