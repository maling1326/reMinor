from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2 as cv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

name = "Maliq"

@app.get("/")
def root():
    return {"message": f"Hello {name}!"}
    
@app.post("/compress")
async def compress_POST(file: UploadFile = File(...)):
    
    image_bytes = await file.read()

    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv.imdecode(nparr, cv.IMREAD_COLOR)
    
    print(image.shape)
    
    from fastapi.responses import Response
    return Response(
        content=image_bytes,
        media_type=file.content_type
    )
    