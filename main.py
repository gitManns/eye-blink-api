from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

from blink_detector import (
    download_video_from_url,
    detect_blinks,
    classify_blink_health,
)

app = FastAPI()

class VideoURLRequest(BaseModel):
    video_url: str

@app.post("/detect-blink-health-url/")
async def detect_blink_health_from_url(request: VideoURLRequest):
    try:
        video_path = download_video_from_url(request.video_url)
        blink_count = detect_blinks(video_path)
        result = classify_blink_health(blink_count)

        # Clean up
        if os.path.exists(video_path):
            os.remove(video_path)

        return {
            "blink_count": blink_count,
            "blink_status": result["blink_status"],
            "recommendation": result["recommendation"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
