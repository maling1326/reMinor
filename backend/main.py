from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2 as cv
from PIL import Image
import io

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

def compress_to_smaller(img_bgr: np.ndarray, original_bytes: bytes) -> bytes:
    img_rgb = cv.cvtColor(img_bgr, cv.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    
    original_size = len(original_bytes)
    
    # coba dari quality rendah ke tinggi
    # sampai ketemu yang lebih kecil dari aslinya
    for quality in range(85, 10, -5):
        buffer = io.BytesIO()
        pil_img.save(buffer, format="JPEG", quality=quality, optimize=True)
        result = buffer.getvalue()
        
        if len(result) < original_size:
            return result
    
    # kalau semua quality masih lebih besar, return aslinya
    return original_bytes

@app.post("/compress")
async def compress(file: UploadFile = File(...)):
    img_bytes = await file.read()
    img       = decode_image(img_bytes)
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    return Response(
        # content    = encode_image(img_gray),
        content    = compress_to_smaller(img, img_bytes),
        media_type = "image/jpeg"
    )

@app.post("/convert")
async def convert_to_grayscale(file: UploadFile = File(...)):
    img_bytes = await file.read()
    img       = decode_image(img_bytes)
    img_gray  = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    return Response(
        content    = encode_image(img_gray),
        media_type = file.content_type
    )