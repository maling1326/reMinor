"""
FastAPI Backend — Image Compression with Deep Learning
Based on: "Image Compression Based on Deep Learning: A Review"
         Yasin & Abdulazeez, Asian Journal of Research in Computer Science, 2021
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import io
import numpy as np
from PIL import Image
import cv2
import torch
import torchvision.transforms as transforms

# scikit-image untuk PSNR & SSIM (Table 1 di paper)
try:
    from skimage.metrics import peak_signal_noise_ratio, structural_similarity
    SKIMAGE_AVAILABLE = True
except ImportError:
    SKIMAGE_AVAILABLE = False

# CompressAI models
from compressai.zoo import (
    bmshj2018_factorized,
    bmshj2018_hyperprior,
    mbt2018,
    cheng2020_anchor,
)

# ─────────────────────────────────────────────
# App Setup
# ─────────────────────────────────────────────

app = FastAPI(title="Image Compression API — Deep Learning")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# Model Registry
# ─────────────────────────────────────────────

MODEL_REGISTRY = {
    "cheng2020_anchor": {
        "loader": cheng2020_anchor,
        "description": "Deep Convolutional Autoencoder (Cheng et al. 2020)",
        "paper_ref": "[74]",
        "quality_range": [1, 6],
    },
    "mbt2018": {
        "loader": mbt2018,
        "description": "Spatially Adaptive Tiled Network (Minnen et al. 2018)",
        "paper_ref": "[76]",
        "quality_range": [1, 8],
    },
    "bmshj2018_factorized": {
        "loader": bmshj2018_factorized,
        "description": "Factorized Entropy CNN (Ballé et al. 2018)",
        "paper_ref": "CNN end-to-end",
        "quality_range": [1, 8],
    },
    "bmshj2018_hyperprior": {
        "loader": bmshj2018_hyperprior,
        "description": "Hyperprior CNN (Ballé et al. 2018)",
        "paper_ref": "CNN end-to-end",
        "quality_range": [1, 8],
    },
}

_model_cache: dict = {}
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def get_model(model_name: str, quality: int):
    cache_key = f"{model_name}_q{quality}"
    if cache_key not in _model_cache:
        if model_name not in MODEL_REGISTRY:
            raise ValueError(f"Unknown model: {model_name}")
        registry = MODEL_REGISTRY[model_name]
        q_min, q_max = registry["quality_range"]
        quality = max(q_min, min(q_max, quality))
        print(f"[model] Loading {model_name} quality={quality} on {DEVICE}...")
        model = registry["loader"](quality=quality, pretrained=True)
        model.eval()
        model.to(DEVICE)
        _model_cache[cache_key] = model
        print(f"[model] Cached as '{cache_key}'")
    return _model_cache[cache_key]


# ─────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────

def decode_image(base64_str: str) -> Image.Image:
    if "," in base64_str:
        base64_str = base64_str.split(",", 1)[1]
    img_bytes = base64.b64decode(base64_str)
    return Image.open(io.BytesIO(img_bytes)).convert("RGB")


def encode_image(img: Image.Image, fmt: str = "PNG") -> str:
    buffer = io.BytesIO()
    img.save(buffer, format=fmt, optimize=True)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def compress_to_bytes(img: Image.Image, target_quality: int = 75) -> bytes:
    """Compress PIL Image to JPEG bytes using Pillow."""
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=target_quality, optimize=True)
    return buffer.getvalue()


def pad_image_tensor(x: torch.Tensor, multiple: int = 64):
    """Pad tensor so H and W are divisible by multiple."""
    _, _, h, w = x.shape
    pad_h = (multiple - h % multiple) % multiple
    pad_w = (multiple - w % multiple) % multiple
    if pad_h > 0 or pad_w > 0:
        x = torch.nn.functional.pad(x, (0, pad_w, 0, pad_h), mode="reflect")
    return x, (h, w)


def calculate_metrics(original: np.ndarray, reconstructed: np.ndarray) -> dict:
    """
    Calculate PSNR and SSIM — same metrics reported in Table 1 of the paper.
    Falls back to manual calculation if scikit-image not available.
    """
    if SKIMAGE_AVAILABLE:
        psnr_val = float(peak_signal_noise_ratio(original, reconstructed, data_range=255))
        ssim_val = float(structural_similarity(
            original, reconstructed,
            channel_axis=2,
            data_range=255
        ))
    else:
        # Manual PSNR fallback
        mse = np.mean((original.astype(float) - reconstructed.astype(float)) ** 2)
        psnr_val = float(20 * np.log10(255.0 / np.sqrt(mse))) if mse > 0 else 100.0
        # Simplified SSIM fallback
        ssim_val = float(1.0 - (mse / (255.0 ** 2)))

    return {
        "psnr": round(psnr_val, 3),
        "ssim": round(ssim_val, 4),
    }


# ─────────────────────────────────────────────
# Request Models
# ─────────────────────────────────────────────

class CompressRequest(BaseModel):
    image: str
    quality: int = 75

class CompressAIRequest(BaseModel):
    image: str
    quality: int = 3      # 1–8
    model: str = "bmshj2018_factorized"

class ConvertRequest(BaseModel):
    image: str


# ─────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "message": "Image Compression API — Deep Learning",
        "paper": "Image Compression Based on Deep Learning: A Review (Yasin & Abdulazeez, 2021)",
        "available_models": list(MODEL_REGISTRY.keys()),
        "device": DEVICE,
        "skimage_available": SKIMAGE_AVAILABLE,
    }


@app.get("/models")
def list_models():
    return {
        name: {
            "description": info["description"],
            "paper_ref": info["paper_ref"],
            "quality_range": info["quality_range"],
        }
        for name, info in MODEL_REGISTRY.items()
    }


@app.post("/compress")
async def compress_pillow(req: CompressRequest):
    """Pillow JPEG compression — baseline comparison."""
    try:
        img = decode_image(req.image)
        original_np = np.array(img)

        compressed = compress_to_bytes(img, req.quality)
        compressed_size = len(compressed)

        raw_b64 = req.image.split(",", 1)[1] if "," in req.image else req.image
        original_size = len(base64.b64decode(raw_b64))

        reconstructed = Image.open(io.BytesIO(compressed)).convert("RGB")
        reconstructed_np = np.array(reconstructed)
        metrics = calculate_metrics(original_np, reconstructed_np)

        result_b64 = "data:image/jpeg;base64," + base64.b64encode(compressed).decode()

        return {
            "result": result_b64,
            "metrics": {
                **metrics,
                "original_bytes": original_size,
                "compressed_bytes": compressed_size,
                "compression_ratio": round(original_size / max(compressed_size, 1), 2),
            },
            "method": "pillow_jpeg",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Compress error: {str(e)}")


@app.post("/compress-ai")
async def compress_ai(req: CompressAIRequest):
    """
    Deep learning image compression via CompressAI.
    Models correspond to papers reviewed in Yasin & Abdulazeez (2021).
    """
    try:
        img = decode_image(req.image)
        original_np = np.array(img)

        x = transforms.ToTensor()(img).unsqueeze(0).to(DEVICE)
        x_padded, (h_orig, w_orig) = pad_image_tensor(x, multiple=64)

        model = get_model(req.model, req.quality)

        with torch.no_grad():
            enc_out = model.compress(x_padded)

        compressed_bytes = sum(
            len(s) for strings in enc_out["strings"] for s in strings
        )

        with torch.no_grad():
            dec_out = model.decompress(enc_out["strings"], enc_out["shape"])

        x_hat = dec_out["x_hat"].squeeze(0).clamp(0, 1).cpu()
        result_np = (x_hat.numpy().transpose(1, 2, 0) * 255).astype(np.uint8)
        result_np = result_np[:h_orig, :w_orig, :]
        result_img = Image.fromarray(result_np)

        metrics = calculate_metrics(original_np, result_np)

        original_raw_bytes = h_orig * w_orig * 3
        bpp = (compressed_bytes * 8) / max(h_orig * w_orig, 1)

        jpeg_buffer = io.BytesIO()
        result_img.save(jpeg_buffer, format="JPEG", quality=95, optimize=True)
        jpeg_bytes = jpeg_buffer.getvalue()
        jpeg_size = len(jpeg_bytes)
        
        return {
            "result": "data:image/jpeg;base64," + base64.b64encode(jpeg_bytes).decode(),
            "metrics": {
                **metrics,
                "bpp": round(bpp, 4),
                "original_bytes": original_raw_bytes,
                "compressed_bytes": jpeg_size,          # ← ukuran file JPEG aktual
                "bitstream_bytes": compressed_bytes,    # ← bitstream CompressAI (referensi akademis)
                "compression_ratio": round(original_raw_bytes / max(jpeg_size, 1), 2),
            },
            "model": req.model,
            "model_description": MODEL_REGISTRY[req.model]["description"],
            "paper_ref": MODEL_REGISTRY[req.model]["paper_ref"],
            "quality": req.quality,
            "device": DEVICE,
        }

    except torch.cuda.OutOfMemoryError:
        raise HTTPException(status_code=507, detail="GPU OOM. Try smaller image.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CompressAI error: {str(e)}")


@app.post("/convert")
async def convert_grayscale(req: ConvertRequest):
    """Convert to grayscale using OpenCV."""
    try:
        img = decode_image(req.image)
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
        result_img = Image.fromarray(img_cv)
        return {"result": "data:image/png;base64," + encode_image(result_img, "PNG")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Convert error: {str(e)}")