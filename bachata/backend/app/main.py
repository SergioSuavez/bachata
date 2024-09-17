from fastapi import FastAPI, UploadFile, File, HTTPException
from backend.app.services.separation import separate_instruments
from backend.app.services.detection import detect_sections
from backend.app.services.youtube import download_audio
import os

app = FastAPI()

# Define upload directory
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bachata Education API!"}

@app.post("/process-song/")
async def process_song(file: UploadFile = File(...)):
    # Save the uploaded file to disk
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    
    try:
        # Separate instruments using Spleeter
        instruments = separate_instruments(file_location)
        
        # Detect sections (Derencho, Majao, Mambo)
        sections = detect_sections(instruments)
        
        # Return the processed data
        return {"instruments": instruments, "sections": sections}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-youtube/")
async def process_youtube(url: str):
    output_path = os.path.join(UPLOAD_DIR, "downloaded_song.mp3")
    try:
        # Download the audio
        download_audio(url, output_path)
        
        # Process the downloaded audio using separate_instruments (without output_dir)
        instruments = separate_instruments(output_path)
        
        return {"message": "YouTube audio processed successfully", "instruments": instruments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
