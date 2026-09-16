# LinkedIn → Telegram İş İlanı Botu

Türkiye'deki güncel remote veya hibrit yazılım iş ilanlarını takip edip CV'nizle eşleşenleri Telegram'a gönderen otomatik bildirim botu.

Bot, LinkedIn'in herkese açık iş arama uç noktasında 30 hedef unvanı (Software Engineer, .NET Developer, React Developer, Kotlin Developer vb.) son 24 saatte yayımlanan remote/hybrid ilanlar için ayrı ayrı arar. İlanları teknoloji anahtar kelimelerine göre filtreler, daha önce iletilenleri SQLite ile eler ve uygun yeni ilanları 15 dakikada bir Telegram'a gönderir.

## Özellikler

- Remote ve hibrit ilanları LinkedIn üzerinden takip eder.
- React, Python, Docker, SQL, backend ve frontend gibi CV anahtar kelimeleriyle eşleştirir.
- Senior, lead, staff, manager ve yüksek deneyim yılı taleplerini hariç tutar; yalnızca Junior, Associate, Entry Level, Intern vb. açıkça belirtilmiş seviyeleri kabul eder.
- Aynı ilanı tekrar bildirmemek için SQLite kullanır.
- Telegram'a HTML biçiminde pozisyon, şirket, konum, eşleşmeler ve başvuru bağlantısı gönderir.
- Docker Compose ile çalışır; ilan geçmişi konteyner yeniden başlasa da korunur.

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

Bot başlangıçta hemen bir kontrol yapar, sonra 15 dakikada bir çalışır. Başarıyla Telegram'a iletilen ilan kimlikleri, yerel çalıştırmada `seen_jobs.db` içindeki `seen_jobs` tablosuna kaydedilir.

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
- `Dockerfile` ve `docker-compose.yml`: Konteynerleştirilmiş, kalıcı veri depolamalı çalışma ortamı
