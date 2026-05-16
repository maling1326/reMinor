from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2 as cv
import torch
from PIL import Image
import io
from compressai.zoo import bmshj2018_factorized

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model = bmshj2018_factorized(quality=3, pretrained=True).eval().to(DEVICE)

def decode_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    return cv.imdecode(nparr, cv.IMREAD_COLOR)
    
def encode_image(image, filetype='.jpg'):
    _, buffer = cv.imencode(filetype, image)
    return buffer.tobytes()

def numpy_to_tensor(img_bgr: np.ndarray) -> torch.Tensor:
    img_rgb = cv.cvtColor(img_bgr, cv.COLOR_BGR2RGB)
    tensor  = torch.from_numpy(img_rgb).permute(2, 0, 1).float() / 255.0
    return tensor.unsqueeze(0).to(DEVICE)

def tensor_to_numpy(tensor: torch.Tensor) -> np.ndarray:
    """Konversi tensor float (1,3,H,W) → numpy BGR (H,W,3) uint8."""
    img = tensor.squeeze(0).permute(1, 2, 0).cpu().numpy()
    img = (img * 255).clip(0, 255).astype(np.uint8)
    return cv.cvtColor(img, cv.COLOR_RGB2BGR)

def compress_image(img_bgr: np.ndarray) -> np.ndarray:
    """
    Kompres gambar menggunakan compressAI (bmshj2018_factorized).
    Proses: encode → bitstream → decode → rekonstruksi gambar.
    """
    x = numpy_to_tensor(img_bgr)

    with torch.no_grad():
        # Encode: kompres ke representasi laten
        compressed = model.compress(x)

        # Decode: rekonstruksi dari bitstream
        x_hat = model.decompress(compressed["strings"], compressed["shape"])

    return tensor_to_numpy(x_hat["x_hat"])

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