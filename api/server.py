"""FastAPI Web Server - HTTP API Interface"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import asyncio
import os
from typing import Optional
from main import YouTubeContentPro
from src.logger import setup_logger
import json

logger = setup_logger(__name__)
app = FastAPI(
    title="YouTube Content Pro API",
    description="Profesyonel AI Video Üretim Sistemi",
    version="2.0.0"
)

# Global instance
pro = YouTubeContentPro("config.yaml")

class VideoRequest(BaseModel):
    """Video üretim isteği"""
    topic: str
    duration_minutes: int = 5
    style: str = "documentary"

class VideoResponse(BaseModel):
    """Video üretim yanıtı"""
    video_id: int
    video_path: str
    audio_path: str
    image_count: int
    duration: float

@app.get("/")
async def root():
    """API Bilgileri"""
    return {
        "name": "YouTube Content Pro API",
        "version": "2.0.0",
        "endpoints": {
            "POST /generate-video": "Yeni video oluştur",
            "GET /videos": "Geçmiş videoları listele",
            "GET /video/{video_id}": "Belirli video bilgisi",
            "GET /video/{video_id}/download": "Video dosyasını indir"
        }
    }

@app.post("/generate-video", response_model=VideoResponse)
async def generate_video(request: VideoRequest):
    """Yeni video oluştur (Async)"""
    try:
        logger.info(f"API İstek: Topic={request.topic}, Duration={request.duration_minutes}min, Style={request.style}")
        
        result = await pro.generate_video(
            topic=request.topic,
            duration_minutes=request.duration_minutes,
            style=request.style
        )
        
        return VideoResponse(**result)
        
    except Exception as e:
        logger.error(f"API Hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/videos")
async def list_videos(limit: int = 10):
    """Geçmiş videoları listele"""
    try:
        videos = pro.db.get_videos(limit=limit)
        return {
            "count": len(videos),
            "videos": [
                {
                    "id": v[0],
                    "topic": v[1],
                    "duration": v[2],
                    "style": v[3],
                    "video_path": v[5],
                    "status": v[7],
                    "created_at": v[9]
                }
                for v in videos
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/video/{video_id}")
async def get_video(video_id: int):
    """Belirli video bilgisi"""
    try:
        video = pro.db.get_video_by_id(video_id)
        if not video:
            raise HTTPException(status_code=404, detail="Video bulunamadı")
        
        return {
            "id": video[0],
            "topic": video[1],
            "duration": video[2],
            "style": video[3],
            "script": video[4][:500] + "..." if video[4] else None,
            "audio_path": video[5],
            "video_path": video[6],
            "metadata": json.loads(video[8]) if video[8] else {},
            "status": video[7],
            "created_at": video[9]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/video/{video_id}/download")
async def download_video(video_id: int):
    """Video dosyasını indir"""
    try:
        video = pro.db.get_video_by_id(video_id)
        if not video or not video[6]:
            raise HTTPException(status_code=404, detail="Video dosyası bulunamadı")
        
        video_path = video[6]
        if not os.path.exists(video_path):
            raise HTTPException(status_code=404, detail="Dosya sistemde bulunamadı")
        
        return FileResponse(
            path=video_path,
            media_type="video/mp4",
            filename=os.path.basename(video_path)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    """Sistem durumu kontrolü"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "database": "ok" if os.path.exists(pro.db.db_path) else "error"
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("FastAPI Server başlatılıyor...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
