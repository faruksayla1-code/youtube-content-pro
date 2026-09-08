import sqlite3
import json
from datetime import datetime
from pathlib import Path
from src.logger import setup_logger

logger = setup_logger(__name__)

class DatabaseManager:
    """Video ve metadata veritabanı yönetimi"""
    
    def __init__(self, db_path="video_generator.db"):
        self.db_path = db_path
        self.init_db()
        logger.info(f"Database başlatıldı - Dosya: {db_path}")
    
    def init_db(self):
        """Veritabanı tabloları oluştur"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                duration_minutes INTEGER,
                style TEXT,
                script TEXT,
                audio_path TEXT,
                video_path TEXT,
                metadata JSON,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER,
                image_path TEXT,
                source_url TEXT,
                file_size INTEGER,
                resolution TEXT,
                downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (video_id) REFERENCES videos(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id INTEGER,
                title TEXT,
                description TEXT,
                hashtags TEXT,
                keywords TEXT,
                thumbnail_text TEXT,
                cta TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (video_id) REFERENCES videos(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Veritabanı tabloları oluşturuldu/kontrol edildi")
    
    def save_video(self, topic, duration, style, script, audio_path, video_path, metadata=None):
        """Video kaydını veritabanına ekle"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO videos (topic, duration_minutes, style, script, audio_path, video_path, metadata, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (topic, duration, style, script, audio_path, video_path, json.dumps(metadata or {}), "completed"))
        
        video_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Video kaydı oluşturuldu - ID: {video_id}")
        return video_id
    
    def get_videos(self, limit=10):
        """Geçmiş videoları getir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM videos ORDER BY created_at DESC LIMIT ?', (limit,))
        videos = cursor.fetchall()
        conn.close()
        
        return videos
    
    def get_video_by_id(self, video_id):
        """Belirli video kaydını getir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM videos WHERE id = ?', (video_id,))
        video = cursor.fetchone()
        conn.close()
        
        return video
