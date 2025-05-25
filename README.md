# Basit HTTP Sunucusu (Socket ile)

## Özellikler
- `GET` isteklerini işler
- `/static` altından dosya sunar
- `/api/hello` endpoint'i JSON döndürür
- MIME type yönetimi vardır

## Docker ile Çalıştırma
```bash
docker build -t http-server .
docker run -p 8080:8080 http-server
