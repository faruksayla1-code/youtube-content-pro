import os
import json
import shutil
from pathlib import Path
from src.logger import setup_logger

logger = setup_logger(__name__)

def cleanup_temp_files(temp_dir="temp"):
    """Geçici dosyaları temizle"""
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            logger.info(f"Geçici dosyalar temizlendi: {temp_dir}")
    except Exception as e:
        logger.warning(f"Geçici dosya temizleme hatası: {e}")

def format_duration(seconds):
    """Saniyeyi dakika:saniye formatına çevir"""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"

def save_json(data, filepath):
    """JSON dosyasını kaydet"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"JSON kaydedildi: {filepath}")

def load_json(filepath):
    """JSON dosyasını yükle"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_file_size(filepath):
    """Dosya boyutunu MB cinsinden döndür"""
    return os.path.getsize(filepath) / (1024 * 1024)

def print_banner():
    """Uygulama başlık bannerı"""
    banner = """
╔═════════════════════════════════════════════════════════════════════════╗
║                                                                         ║
║   🎬 YOUTUBE CONTENT PRO - Profesyonel Video Üretim Sistemi v2.0      ║
║                                                                         ║
║   Ollama + Edge TTS + Advanced AI Features                             ║
║                                                                         ║
╚═════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)
