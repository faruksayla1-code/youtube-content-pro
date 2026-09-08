import time
import ollama
from src.logger import setup_logger

logger = setup_logger(__name__)

class AIScriptGenerator:
    """Ollama tabanlı profesyonel senaryo üretici"""
    
    def __init__(self, model="qwen3-turkish:latest", temperature=0.7):
        self.model = model
        self.temperature = temperature
        logger.info(f"AI Agent başlatıldı - Model: {model}")
    
    def generate_script(self, topic, duration_minutes, style="documentary"):
        """Profesyonel, bölümlü senaryo üret"""
        logger.info(f"Senaryo üretimi başladı - Konu: {topic}, Süre: {duration_minutes}dk, Stil: {style}")
        start_time = time.time()
        
        # İleri prompt engineering
        styles = {
            "documentary": "akademik, ciddi, bilgilendirici tonu",
            "educational": "eğitici, anlaşılır, basit yapılı",
            "dramatic": "dramatik, etkileyici, duygusal",
            "romantic": "nazik, şiirsel, duygusal anlatım"
        }
        
        tone = styles.get(style, styles["documentary"])
        
        prompt = f"""Konu: {topic}
Hedef Süre: Yaklaşık {duration_minutes} dakika
Ton: {tone}

Bu konu için profesyonel bir YouTube belgesel senaryosu yaz. 
Senaryoyu şu dört net bölüme kurgula:

1. AÇILIŞ & KANCA (ilk 30 saniye)
   - Dikkat çeken bir soru veya ifade
   - Konunun neden önemli olduğu
   - Neleri öğreneceği

2. TARİHSEL KÖKLER & ARKAPLAN (ilk 1/3 kısım)
   - Tarihsel bağlam
   - Önemli tarihler ve olaylar
   - Kültürel/mimari yapı

3. KRİTİK DÖNEMLER & DETAYLAR (orta 1/3 kısım)
   - Önemli dönüm noktaları
   - İlginç ayrıntılar
   - İnsan hikayeleri

4. KAPANIŞ & ETKI (son 30 saniye)
   - Öğrenilen dersleri özetle
   - Modern bağlantı
   - Yapılacak çağrı (beğen, abone ol)

KEYFİYETLER:
- Akıcı, doğal konuşma dili kullan
- SEO anahtar kelimeleri doğal şekilde yerleştir
- Kesinlikle sahne numarası, yönetmen notu veya HTML tag'ı ekleme
- Yalnızca seslendirilecek pürüzsüz anlatım metnini ver
- Dramatik duraklamalar için [DURAKLAMA] işareti kullan
- Tonlama değişiklikleri için [TONLAMA: X] kullan
"""
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                stream=False,
                options={'temperature': self.temperature}
            )
            
            script = response['message']['content']
            elapsed = time.time() - start_time
            
            logger.info(f"Senaryo başarıyla üretildi ({elapsed:.2f}s) - Karakter: {len(script)}")
            return script
            
        except Exception as e:
            logger.error(f"Senaryo üretim hatası: {e}")
            raise
    
    def generate_metadata(self, topic, script):
        """YouTube metadatası üret (başlık, açıklama, hashtag)"""
        logger.info(f"Metadata üretimi başladı - Konu: {topic}")
        
        prompt = f"""Konu: {topic}
Senaryo başlangıcı: {script[:500]}...

Bu video için aşağıdakileri JSON formatında üret:

1. title: YouTube başlığı (60 karakter max, SEO optimized)
2. description: Video açıklaması (2-3 paragraf, SEO keywords içeren)
3. hashtags: 15 adet ilgili hashtag (trending)
4. keywords: 10 adet SEO anahtar kelimesi
5. thumbnail_text: Thumbnail yazısı (kısa ve çarpıcı)
6. cta: Call-to-action önerisi

JSON formatında döndür, başka metin ekleme:
"""
        
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                stream=False
            )
            
            logger.info("Metadata başarıyla üretildi")
            return response['message']['content']
            
        except Exception as e:
            logger.error(f"Metadata üretim hatası: {e}")
            return None
