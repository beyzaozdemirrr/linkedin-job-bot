# LinkedIn to Telegram - Akıllı İş İlanı Avcısı

Türkiye'deki Remote ve Hybrid yazılım fırsatlarını takip etmek için geliştirilmiş, Junior/Mid seviyeye odaklı otomatik bir bildirim botudur. LinkedIn üzerindeki ilanlar arasından CV'nizle uyuşan ve Senior/Lead süzgecinden geçen yeni fırsatları 15 dakikada bir doğrudan Telegram kanalınıza iletir.

## Projenin Amacı ve Çalışma Mantığı

Manuel olarak sürekli LinkedIn'de arama yapma ihtiyacını ortadan kaldırır:

1. **Geniş Ağ Tarar:** 30 farklı iş başlığını (`Software Engineer`, `Full Stack Developer`, `.NET`, `React`, `Kotlin Developer` vb.) döngüsel olarak tarar.
2. **Süzgeç Uygular:**
* `Senior`, `Lead`, `Manager`, `5+ years` gibi tecrübe şartı yüksek ilanları eler.
* `Junior`, `Entry Level`, `Associate`, `New Grad` ve stajyer seviyesindeki ilanları seçer.
* İlan metninde belirlediğiniz teknolojilerin (`MERN`, `React`, `Node.js`, `ASP.NET Core`, `Docker`, `SQL`, `Kotlin` vb.) geçip geçmediğini doğrular.


3. **Duplicate Kayıt Engeller:** Daha önce bildirdiği ilanları SQLite veritabanında saklar, aynı bildirimi tekrar göndermez.

## Mimari ve Tech Stack

* **Python 3.11 & BeautifulSoup4:** LinkedIn public sayfalarından hafif HTML parsing işlemleri.
* **SQLite:** Duplicate bildirimleri engellemek için hafif veri saklama katmanı.
* **APScheduler:** 15 dakikalık periyotlarla tarama döngüsünü yöneten zamanlayıcı.
* **Telegram Bot API:** Uygun ilanları başlık, şirket, konum ve başvuru linkiyle ileten entegrasyon.
* **Docker & Docker Compose:** İzolasyon içinde 7/24 kesintisiz çalışma ve `volume` desteğiyle kalıcı veri (persistence) yönetimi.

## Proje Yapısı

```text
├── main.py              # APScheduler ile 15 dk'lık zamanlayıcı ve ana iş akışı
├── linkedin_scraper.py  # 30 farklı unvanı sırayla tarayan LinkedIn scraper'ı
├── filters.py           # Seviye (Junior/Mid) ve teknoloji eşleşme mantığı
├── db.py                # SQLite veri kayıt ve duplicate kontrol katmanı
├── telegram_notifier.py # Telegram HTML formatlı mesaj gönderici
├── config.py            # Arama parametreleri, anahtar kelimeler ve .env konfigürasyonu
├── Dockerfile           # Non-root (appuser) güvenlikli Docker yapılandırması
└── docker-compose.yml   # Volume ve container orkestrasyonu

```

## Hızlı Kurulum

### 1. Yerel Ortamda Çalıştırma (Local)

```powershell
# Sanal ortam oluşturun ve aktif edin
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Linux/Mac için: source .venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Çevre değişkenlerini hazırlayın
Copy-Item .env.example .env     # Linux/Mac için: cp .env.example .env

```

`.env` dosyasının içine kendi **Telegram Bot Token** ve **Chat ID** bilgilerinizi girin, ardından başlatın:

```powershell
python main.py

```

### 2. Docker ile Çalıştırma

Hassas bilgilerinizi (`.env`) image içine gömmeden çalıştırmak için:

```powershell
docker compose up --build -d

```

`seen_jobs_data` volume'u sayesinde konteyner silinse veya baştan kurulsa bile taranan ilan geçmişiniz (`seen_jobs.db`) korunur.

**Logları canlı izlemek için:**

```powershell
docker compose logs -f job-bot

```

## Güvenlik

* `.env` dosyası ve `.db` veritabanı `.gitignore` ile korumaya alınmıştır; gizli anahtarlar Git'e dahil edilmez.
* Docker konteyneri root yetkisi yerine kısıtlı `appuser` (UID 10001) ile çalışır.
* Örnek yapı `.env.example` dosyası üzerinden sağlanır.
