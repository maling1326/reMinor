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

def compress_image(img_bgr: np.ndarray, quality=85) -> bytes:
    img_rgb = cv.cvtColor(img_bgr, cv.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)

    buffer = io.BytesIO()
    pil_img.save(
        buffer,
        format="JPEG",
        quality=quality,
        optimize=True,
        progressive=True
    )
    return buffer.getvalue()

@app.post("/compress")
async def compress(file: UploadFile = File(...)):
    img_bytes = await file.read()
    img       = decode_image(img_bytes)

    return Response(
        content    = compress_image(img),
        media_type = file.content_type
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