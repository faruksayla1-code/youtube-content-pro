import asyncio
import edge_tts
import time
from src.logger import setup_logger

logger = setup_logger(__name__)

class AudioEngine:
    """Profesyonel ses sentezi motoru"""
    
    def __init__(self, voice="tr-TR-AhmetNeural"):
        self.voice = voice
        logger.info(f"Audio Engine başlatıldı - Ses: {voice}")
    
    async def create_voiceover(self, text, output_path="ses.mp3", rate=1.0):
        """Metin'i profesyonel Türkçe sese dönüştür"""
        logger.info(f"Ses üretimi başladı - Çıktı: {output_path}")
        start_time = time.time()
        
        try:
            # Rate formatı: +50% = "1.5" veya "-25%" = "-25"
            rate_str = f"{int((rate - 1) * 100):+d}%" if rate != 1.0 else "+0%"
            
            communicate = edge_tts.Communicate(
                text=text,
                voice=self.voice,
                rate=rate_str
            )
            
            await communicate.save(output_path)
            
            elapsed = time.time() - start_time
            logger.info(f"Ses dosyası başarıyla kaydedildi ({elapsed:.2f}s) - Dosya: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Ses üretim hatası: {e}")
            raise
    
    async def process_script_with_marks(self, script):
        """[DURAKLAMA] ve [TONLAMA] işaretlerini işle"""
        # Şimdilik basit versiyon - SSML desteği eklenebilir
        processed = script.replace("[DURAKLAMA]", "...").replace("[TONLAMA:", "")
        return processed
