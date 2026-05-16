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

def decode_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    return cv.imdecode(nparr, cv.IMREAD_COLOR)
    
def encode_image(image, filetype='.jpg'):
    _, buffer = cv.imencode(filetype, image)
    return buffer.tobytes()

def compress_image(img, quality=50):
    return img

@app.post("/compress")
async def compress(file: UploadFile = File(...)):
    
    img_bytes = await file.read()

    img            = decode_image(img_bytes)
    img_compressed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # img_compressed = compress_image(img)
    
    from fastapi.responses import Response
    return Response(
        content    = encode_image(img_compressed),
        media_type = file.content_type
    )
    
@app.post("/convert")
async def convert_to_grayscale(file: UploadFile = File(...)):
    
    img_bytes = await file.read()

    img            = decode_image(img_bytes)
    img_compressed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    from fastapi.responses import Response
    return Response(
        content    = encode_image(img_compressed),
        media_type = file.content_type
    )