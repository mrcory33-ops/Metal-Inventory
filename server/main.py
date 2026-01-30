"""
Kokoro TTS Server for Metal Inventory Application
Exposes a simple REST API for text-to-speech conversion.
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from kokoro import KPipeline
import numpy as np
import soundfile as sf
import io
import os

app = FastAPI(title="Kokoro TTS Server", version="1.0.0")

# Allow CORS for Firebase Hosting frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to your Firebase domain
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Initialize Kokoro pipeline (lazy load on first request)
pipeline = None

def get_pipeline():
    global pipeline
    if pipeline is None:
        print("Initializing Kokoro pipeline...")
        pipeline = KPipeline(lang_code='a')  # 'a' for American English
        print("Kokoro pipeline ready!")
    return pipeline


@app.get("/")
async def health_check():
    """Health check endpoint for Cloud Run."""
    return {"status": "healthy", "service": "kokoro-tts"}


@app.get("/tts")
async def text_to_speech(
    text: str = Query(..., description="Text to convert to speech"),
    voice: str = Query("af_heart", description="Voice to use (af_heart, am_adam, bf_emma, bm_george)")
):
    """
    Convert text to speech using Kokoro TTS.
    Returns WAV audio stream.
    """
    if not text or len(text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text parameter is required")
    
    if len(text) > 1000:
        raise HTTPException(status_code=400, detail="Text too long (max 1000 characters)")
    
    try:
        pipe = get_pipeline()
        
        # Generate audio chunks
        audio_chunks = []
        for _, _, audio in pipe(text, voice=voice):
            audio_chunks.append(audio)
        
        if not audio_chunks:
            raise HTTPException(status_code=500, detail="No audio generated")
        
        # Combine all chunks
        combined_audio = np.concatenate(audio_chunks)
        
        # Write to WAV buffer
        buffer = io.BytesIO()
        sf.write(buffer, combined_audio, 24000, format='wav')
        buffer.seek(0)
        
        return StreamingResponse(
            buffer,
            media_type="audio/wav",
            headers={"Content-Disposition": "inline; filename=speech.wav"}
        )
    
    except Exception as e:
        print(f"TTS Error: {e}")
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {str(e)}")


@app.get("/voices")
async def list_voices():
    """List available voices."""
    return {
        "voices": [
            {"code": "af_heart", "name": "Heart", "gender": "female", "accent": "american"},
            {"code": "af_bella", "name": "Bella", "gender": "female", "accent": "american"},
            {"code": "am_adam", "name": "Adam", "gender": "male", "accent": "american"},
            {"code": "am_michael", "name": "Michael", "gender": "male", "accent": "american"},
            {"code": "bf_emma", "name": "Emma", "gender": "female", "accent": "british"},
            {"code": "bm_george", "name": "George", "gender": "male", "accent": "british"},
        ]
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
