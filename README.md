# 🎬 YouTube Content Pro - Profesyonel Video Üretim Sistemi

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.9+-blue)

AI-powered, tam otomatik YouTube video üretim sistemi. Ollama, Edge TTS ve Advanced Features ile profesyonel seviye videolar oluştur.

## ✨ Özellikler

- 🤖 **AI Senaryo Yazma** - Ollama ile akıllı script üretimi
- 🎙️ **Profesyonel Ses** - Edge TTS ile doğal Türkçe narasyonlar
- 🖼️ **Otomatik Görsel** - DuckDuckGo ile yüksek kaliteli görseller
- 🎥 **Video Montajı** - MoviePy ile sinematik video oluşturma
- 📊 **SEO Optimizasyonu** - Başlık, açıklama, hashtag üretimi
- 💾 **Veritabanı** - Geçmiş videoları takip etme
- ⚙️ **Yapılandırılabilir** - config.yaml ile tam kontrol
- 📝 **Detaylı Logging** - Her işlemin kaydı

## 🚀 Kurulum

### Gereksinimler
- Python 3.9+
- Ollama (https://ollama.ai)
- FFmpeg

### Adım 1: Repository'i Clone Et

```bash
git clone https://github.com/faruksayla1-code/youtube-content-pro.git
cd youtube-content-pro
```

### Adım 2: Virtual Environment Oluştur

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### Adım 3: Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### Adım 4: Ollama Modeli Yükle

```bash
ollama pull qwen3-turkish:latest
```

### Adım 5: FFmpeg Yükle

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
[ffmpeg.org](https://ffmpeg.org/download.html) adresinden indir

## 📖 Kullanım

### Basit Kullanım

```bash
python main.py
```

Sonra konuyu ve süreyi gir.

### Örnekler

```bash
# Varsayılan ayarlarla
python main.py

# Doğrudan kodu çalıştır
python -c "from main import YouTubeContentPro; import asyncio; pro = YouTubeContentPro(); asyncio.run(pro.generate_video('İznik Tarihi', 5, 'documentary'))"
```

## ⚙️ Yapılandırma

`config.yaml` dosyasını düzenleyerek ayarları özelleştir:

```yaml
ollama:
  model: "qwen3-turkish:latest"  # Ollama model
  temperature: 0.7  # Yaratıcılık (0-1)

audio:
  voice: "tr-TR-AhmetNeural"  # Ses seçimi
  rate: 1.0  # Ses hızı

video:
  fps: 24  # Frame rate
  preset: "medium"  # Encode hızı

image_processing:
  max_images: 35  # Max görsel sayısı
  min_file_size: 15360  # Minimum dosya boyutu
```

## 📁 Proje Yapısı

```
youtube-content-pro/
├── main.py              # Ana giriş noktası
├── config.yaml          # Yapılandırma
├── requirements.txt     # Bağımlılıklar
├── src/
│   ├── ai_agent.py      # Ollama entegrasyonu
│   ├── audio_engine.py  # TTS/ses işleme
│   ├── media_manager.py # Görsel/video yönetimi
│   ├── database.py      # SQLite veritabanı
│   ├── logger.py        # Logging sistemi
│   └── utils.py         # Yardımcı fonksiyonlar
├── output_videos/       # Oluşturulan videolar
├── logs/                # Log dosyaları
└── README.md
```

## 🔧 Gelişmiş Kullanım

### Python Kodu İçinde Kullanım

```python
from main import YouTubeContentPro
import asyncio

async def create_video():
    pro = YouTubeContentPro("config.yaml")
    result = await pro.generate_video(
        topic="İznik Osmanlı Müzesi",
        duration_minutes=10,
        style="documentary"
    )
    print(f"Video: {result['video_path']}")

asyncio.run(create_video())
```

### API Server Çalıştır (FastAPI)

```bash
python api/server.py
```

Sonra `http://localhost:8000` adresine POST isteği gönder:

```bash
curl -X POST "http://localhost:8000/generate-video" \
  -H "Content-Type: application/json" \
  -d '{"topic": "İznik Tarihi", "duration": 5, "style": "documentary"}'
```

## 📊 Veritabanı

Üretilen videolar SQLite veritabanına kaydedilir. Sorgulamak için:

```python
from src.database import DatabaseManager

db = DatabaseManager()
videos = db.get_videos(limit=10)
for video in videos:
    print(f"ID: {video[0]}, Konu: {video[1]}, Tarih: {video[9]}")
```

## 🐛 Sorun Giderme

### Ollama Bağlantı Hatası
```
Ollama Server'ın çalıştığını kontrol et:
ollama serve
```

### FFmpeg Bulunamadı
```
FFmpeg'i sisteme ekle:
sudo apt-get install ffmpeg  # Linux
brew install ffmpeg  # macOS
```

### Ses Sentezi Hatası
```
Internet bağlantınızı kontrol et (Edge TTS internet gerektirir)
```

## 📝 Loglar

Tüm işlemler `logs/app.log` dosyasına kaydedilir. Detaylı debugging için:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🎯 Roadmap

- [ ] Stable Diffusion entegrasyonu (görsel üretimi)
- [ ] YouTube otomatik yükleme
- [ ] Web dashboard
- [ ] Batch işleme
- [ ] Voice cloning
- [ ] Daha fazla dil desteği
- [ ] İstatistikler ve analizler

## 📄 Lisans

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 👤 Yazar

**Faruk Sayla**
- GitHub: [@faruksayla1-code](https://github.com/faruksayla1-code)

## 🤝 Katkıda Bulun

Pull request'ler hoşça karşılanır!

```bash
git clone <repo-url>
git checkout -b feature/AmazingFeature
git commit -m 'Add some AmazingFeature'
git push origin feature/AmazingFeature
```

## ⭐ Destek

Projeyi beğendiysen yıldız ver! ⭐

---

**Sorunlar veya öneriler için:** [Issues](https://github.com/faruksayla1-code/youtube-content-pro/issues) sayfasını ziyaret et.
