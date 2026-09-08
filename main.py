#!/usr/bin/env python3
"""
YouTube Content Pro - Ana Giriş Noktası
Profesyonel AI-powered video üretim sistemi
"""

import asyncio
import os
import sys
import time
from pathlib import Path

from src.utils import print_banner, cleanup_temp_files, save_json, format_duration
from src.ai_agent import AIScriptGenerator
from src.audio_engine import AudioEngine
from src.media_manager import MediaManager
from src.database import DatabaseManager
from src.logger import setup_logger
import yaml

logger = setup_logger(__name__)

class YouTubeContentPro:
    """Profesyonel video üretim sistemi"""
    
    def __init__(self, config_path="config.yaml"):
        """Sistemi başlat"""
        self.config = self.load_config(config_path)
        self.ai_agent = AIScriptGenerator(
            model=self.config['ollama']['model'],
            temperature=self.config['ollama']['temperature']
        )
        self.audio_engine = AudioEngine(
            voice=self.config['audio']['voice']
        )
        self.media_manager = MediaManager(
            output_dir=self.config['output']['video_dir'],
            temp_dir=self.config['output']['temp_dir']
        )
        self.db = DatabaseManager(
            db_path=self.config['database']['path']
        )
        logger.info("YouTube Content Pro sistemi başlatıldı")
    
    def load_config(self, config_path):
        """Konfigürasyonu yükle"""
        if not os.path.exists(config_path):
            logger.warning(f"Config dosyası bulunamadı: {config_path}")
            return {}
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    async def generate_video(self, topic, duration_minutes=5, style="documentary"):
        """Tam video üret"""
        total_start = time.time()
        logger.info(f"\n{'='*70}")
        logger.info(f"Video üretimi başlatıldı")
        logger.info(f"Konu: {topic}")
        logger.info(f"Süre: {duration_minutes} dakika")
        logger.info(f"Stil: {style}")
        logger.info(f"{'='*70}\n")
        
        try:
            # 1. Senaryo üret
            logger.info("[1/5] Senaryo üretiliyor...")
            script = self.ai_agent.generate_script(topic, duration_minutes, style)
            
            # 2. Metadata üret
            logger.info("[2/5] Metadata üretiliyor...")
            metadata_text = self.ai_agent.generate_metadata(topic, script)
            
            # 3. Ses üret
            logger.info("[3/5] Ses sentezi yapılıyor...")
            audio_path = os.path.join(self.config['output']['temp_dir'], "voiceover.mp3")
            await self.audio_engine.create_voiceover(script, audio_path)
            
            # 4. Görselleri indir
            logger.info("[4/5] Görseller indiriliyor...")
            max_images = self.config['image_processing']['max_images']
            image_paths = self.media_manager.fetch_images(
                topic,
                max_images=max_images,
                min_file_size=self.config['image_processing']['min_file_size']
            )
            
            if not image_paths:
                raise ValueError("Yeterli görsel indirilemedi")
            
            # 5. Video oluştur
            logger.info("[5/5] Video oluşturuluyor...")
            video_name = f"{topic.replace(' ', '_')}_{int(time.time())}.mp4"
            video_path = self.media_manager.create_video(
                image_paths,
                audio_path,
                video_name,
                fps=self.config['video']['fps']
            )
            
            # Veritabanına kaydet
            video_id = self.db.save_video(
                topic=topic,
                duration=duration_minutes,
                style=style,
                script=script,
                audio_path=audio_path,
                video_path=video_path,
                metadata={'metadata': metadata_text}
            )
            
            # Sonuç
            elapsed = time.time() - total_start
            logger.info(f"\n{'='*70}")
            logger.info(f"✅ VIDEO BAŞARIYLA OLUŞTURULDU!")
            logger.info(f"{'='*70}")
            logger.info(f"Video ID: {video_id}")
            logger.info(f"Çıktı: {video_path}")
            logger.info(f"Toplam Süre: {format_duration(elapsed)}")
            logger.info(f"{'='*70}\n")
            
            return {
                'video_id': video_id,
                'video_path': video_path,
                'audio_path': audio_path,
                'image_count': len(image_paths),
                'metadata': metadata_text,
                'duration': elapsed
            }
            
        except Exception as e:
            logger.error(f"Video üretim hatası: {e}", exc_info=True)
            raise
        finally:
            # Geçici dosyaları temizle (opsiyonel)
            # cleanup_temp_files(self.config['output']['temp_dir'])
            pass

async def main():
    """Ana fonksiyon"""
    print_banner()
    
    try:
        # Sistemi başlat
        pro = YouTubeContentPro("config.yaml")
        
        # Kullanıcıdan girdi al
        print("\n📝 Video Detaylarını Gir:")
        print("-" * 50)
        
        topic = input("Videomuzun konusu nedir? : ").strip()
        if not topic:
            topic = "Anadolu'nun Antik Gizemleri"
            print(f"(Varsayılan: {topic})")
        
        duration_str = input("Hedef süre (dakika cinsinden, varsayılan: 5): ").strip()
        try:
            duration = int(duration_str) if duration_str else 5
        except ValueError:
            duration = 5
            print(f"(Varsayılan: {duration}dk)")
        
        style = input("Video stili (documentary/educational/dramatic/romantic, varsayılan: documentary): ").strip()
        if style not in ["documentary", "educational", "dramatic", "romantic"]:
            style = "documentary"
            print(f"(Varsayılan: {style})")
        
        print(f"\n🚀 Video üretimi başlatılıyor...\n")
        
        # Video üret
        result = await pro.generate_video(topic, duration, style)
        
        print(f"\n✨ Tamamlandı! Video şurada: {result['video_path']}")
        
    except KeyboardInterrupt:
        logger.info("\n[İPTAL] İşlem kullanıcı tarafından durduruldu.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
