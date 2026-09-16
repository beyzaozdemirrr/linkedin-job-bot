# LinkedIn → Telegram İş İlanı Botu

Bu bot, LinkedIn'in herkese açık iş arama uç noktasında Türkiye'deki son 24 saatlik remote/hybrid `Software Engineer` ilanlarını kontrol eder. CV anahtar kelimeleriyle eşleşen yeni ilanları Telegram'a gönderir ve tekrarları SQLite'ta engeller.

## Kurulum

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env` içindeki `TELEGRAM_TOKEN` ile `CHAT_ID` (veya `TELEGRAM_CHAT_ID`) değerlerini doldurun. Ardından:

```powershell
python main.py
```

Bot başlangıçta hemen bir kontrol yapar, sonra 15 dakikada bir çalışır. Başarıyla Telegram'a iletilen ilan kimlikleri `jobs.db` içindeki `seen_jobs` tablosuna kaydedilir.

## Docker ile çalıştırma

`.env` dosyasını image'e kopyalamadan, yalnızca konteynere çalışma anında aktararak başlatın:

```powershell
docker compose up --build -d
```

`seen_jobs_data` named volume'u, `/app/data/seen_jobs.db` dosyasını konteyner yeniden başlatılsa da korur. Günlükleri görmek için `docker compose logs -f job-bot` kullanın.

## Dosyalar

- `config.py`: LinkedIn araması, anahtar kelimeler ve ortam değişkenleri
- `linkedin_scraper.py`: Herkese açık LinkedIn sonuç kartlarını ayrıştırır
- `filters.py`: Hariç tutma ve CV eşleşme kuralı
- `database.py`: SQLite tekrar engelleme katmanı
- `telegram_notifier.py`: Telegram HTML mesajı
- `main.py`: APScheduler iş akışı
