from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os
from blink_detector import count_blinks_and_duration

app = FastAPI()

def get_recommendations(blinks_per_minute):
    if blinks_per_minute >= 15:
        return [
            "Blink rate is healthy — keep maintaining good screen habits.",
            "Ensure regular outdoor time to reduce myopia risk.",
            "Follow the 20-20-20 rule to rest your eyes: every 20 minutes, look at something 20 feet away for 20 seconds."
        ]
    elif 10 <= blinks_per_minute < 15:
        return [
            "Blink rate is slightly low — consider taking more frequent breaks.",
            "Consciously blink more during screen use to maintain tear film health.",
            "Try reducing screen brightness and improving ambient lighting."
        ]
    else:
        return [
            "Blink rate is low — you may be at risk of digital eye strain or early myopia.",
            "Take a break every 20 minutes and look away from the screen.",
            "Ensure you blink regularly and keep your screen at proper distance and height.",
            "Consider scheduling an eye exam if symptoms persist."
        ]

@app.post("/detect-blink-health/")
async def detect_blink_health(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        temp_file = "temp_video.mp4"

        with open(temp_file, "wb") as f:
            f.write(contents)

        blink_count, duration_seconds = count_blinks_and_duration(temp_file)
        os.remove(temp_file)

        if duration_seconds == 0:
            return JSONResponse(
                status_code=400,
                content={"error": "Video duration is zero or unreadable."}
            )

        bpm = (blink_count / duration_seconds) * 60
        status = "Healthy" if bpm >= 15 else "Low Blink Rate - At Risk" if bpm < 10 else "Borderline"

        return {
            "blink_count": blink_count,
            "duration_seconds": round(duration_seconds, 2),
            "blinks_per_minute": round(bpm, 2),
            "blink_status": status,
            "recommendations": get_recommendations(bpm)
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Something went wrong: {str(e)}"}
        )
