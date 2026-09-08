import os
import requests
import asyncio
from pathlib import Path
from duckduckgo_search import DDGS
from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips
from PIL import Image
from src.logger import setup_logger
import time

logger = setup_logger(__name__)

class MediaManager:
    """Görsel ve video yönetimi"""
    
    def __init__(self, output_dir="output_videos", temp_dir="temp"):
        self.output_dir = output_dir
        self.temp_dir = temp_dir
        self.image_dir = os.path.join(temp_dir, "images")
        
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.image_dir, exist_ok=True)
        logger.info(f"Media Manager başlatıldı")
    
    def fetch_images(self, query, max_images=35, min_file_size=15360):
        """Yüksek kaliteli görselleri indir"""
        logger.info(f"Görsel taraması başladı - Sorgu: {query}, Max: {max_images}")
        start_time = time.time()
        
        image_paths = []
        search_queries = [
            f"{query} cinematic history documentation high resolution",
            f"{query} historic architecture landscape 4k",
            f"{query} cultural heritage museum exhibition",
            f"{query} ancient ruins archaeological site"
        ]
        
        with DDGS() as ddgs:
            for q in search_queries:
                if len(image_paths) >= max_images:
                    break
                    
                try:
                    results = ddgs.images(q, max_results=max_images // len(search_queries) + 5)
                    
                    for res in results:
                        if len(image_paths) >= max_images:
                            break
                        
                        try:
                            img_url = res.get('image')
                            if not img_url:
                                continue
                            
                            img_data = requests.get(img_url, timeout=5).content
                            
                            # Boyut kontrolü
                            if len(img_data) < min_file_size:
                                logger.debug(f"Görsel filtrelendi (çok küçük): {len(img_data)} bytes")
                                continue
                            
                            # Kaydet
                            img_path = os.path.join(self.image_dir, f"img_{len(image_paths):03d}.jpg")
                            with open(img_path, 'wb') as f:
                                f.write(img_data)
                            
                            # Doğrula
                            try:
                                img = Image.open(img_path)
                                if img.size[0] < 640 or img.size[1] < 480:
                                    os.remove(img_path)
                                    logger.debug(f"Görsel filtrelendi (düşük çözünürlük): {img.size}")
                                    continue
                            except:
                                os.remove(img_path)
                                continue
                            
                            image_paths.append(img_path)
                            logger.debug(f"Görsel eklendi: {len(image_paths)}/{max_images}")
                            
                        except Exception as e:
                            logger.debug(f"Görsel indirme hatası: {e}")
                            continue
                            
                except Exception as e:
                    logger.warning(f"Arama hatası ({q}): {e}")
                    continue
        
        elapsed = time.time() - start_time
        logger.info(f"Görsel taraması tamamlandı ({elapsed:.2f}s) - Toplam: {len(image_paths)}")
        return image_paths
    
    def create_video(self, image_paths, audio_path, output_name="video.mp4", fps=24):
        """Görsel + Sesi birleştir ve video oluştur"""
        logger.info(f"Video oluşturma başladı - Çıktı: {output_name}")
        start_time = time.time()
        
        if not image_paths:
            logger.error("Görsel bulunamadı!")
            raise ValueError("En az bir görsel gerekli")
        
        try:
            # Ses yükle
            audio_clip = AudioFileClip(audio_path)
            audio_duration = audio_clip.duration
            logger.info(f"Ses yüklendi - Süre: {audio_duration:.2f}s ({audio_duration/60:.2f}dk)")
            
            # Görsel başına süre
            clip_duration = audio_duration / len(image_paths)
            logger.info(f"Görsel başına süre: {clip_duration:.2f}s")
            
            # Klipleri oluştur
            clips = []
            for i, img_path in enumerate(image_paths):
                try:
                    img_clip = ImageClip(img_path).set_duration(clip_duration)
                    clips.append(img_clip)
                except Exception as e:
                    logger.warning(f"Görsel klip hatası ({img_path}): {e}")
                    continue
            
            if not clips:
                raise ValueError("Klip oluşturulamadı")
            
            # Video derle
            logger.info(f"Video klipleri birleştiriliyor...")
            video = concatenate_videoclips(clips, method="compose")
            video = video.set_audio(audio_clip)
            
            # Çıktı yolu
            output_path = os.path.join(self.output_dir, output_name)
            
            # Render
            logger.info(f"Video render ediliyor (FFmpeg)...")
            video.write_videofile(
                output_path,
                fps=fps,
                codec="libx264",
                audio_codec="aac",
                preset="medium",
                verbose=False,
                logger=None
            )
            
            elapsed = time.time() - start_time
            logger.info(f"Video başarıyla oluşturuldu ({elapsed:.2f}s) - Dosya: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Video oluşturma hatası: {e}")
            raise
