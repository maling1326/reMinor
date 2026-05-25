"""
FastAPI Backend — Image Compression with Deep Learning
Based on: "Image Compression Based on Deep Learning: A Review"
         Yasin & Abdulazeez, Asian Journal of Research in Computer Science, 2021
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import base64
import io
import logging
import time
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image
import cv2
import torch
import torchvision.transforms as transforms

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s — %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

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

# Thread pool — heavy models (mbt2018, cheng2020_anchor) block for minutes on CPU.
# Running them off the event loop prevents FastAPI from freezing and the client
# from receiving a timeout/502 before inference finishes.
_executor = ThreadPoolExecutor(max_workers=2)


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


def get_original_file_bytes(base64_str: str) -> int:
    """Ambil ukuran file asli (bytes) dari base64 string yang dikirim client."""
    raw_b64 = base64_str.split(",", 1)[1] if "," in base64_str else base64_str
    return len(base64.b64decode(raw_b64))


def encode_image(img: Image.Image, fmt: str = "PNG") -> str:
    buffer = io.BytesIO()
    img.save(buffer, format=fmt, optimize=True)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def compress_to_bytes(img: Image.Image, target_quality: int = 75) -> bytes:
    """Compress PIL Image to JPEG bytes using Pillow."""
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=target_quality, optimize=True)
    return buffer.getvalue()


def find_best_jpeg(img: Image.Image, original_size: int) -> bytes:
    """
    Cari JPEG quality tertinggi yang ukuran output-nya lebih kecil dari original.
    Resolusi TIDAK diturunkan sama sekali.
    Urutan quality: 85 → 75 → 65 → 55 → 45 → 35 (fallback terakhir).
    """
    for q in [85, 75, 65, 55, 45, 35]:
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=q, optimize=True, progressive=True)
        data = buf.getvalue()
        if len(data) < original_size:
            return data

    # Absolute fallback — quality terendah
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=30, optimize=True, progressive=True)
    return buf.getvalue()


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
        mse = np.mean((original.astype(float) - reconstructed.astype(float)) ** 2)
        psnr_val = float(20 * np.log10(255.0 / np.sqrt(mse))) if mse > 0 else 100.0
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

        # Ukuran file asli dari bytes yang dikirim
        original_size = get_original_file_bytes(req.image)

        compressed = compress_to_bytes(img, req.quality)
        compressed_size = len(compressed)

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


def _run_compressai_sync(
    img: Image.Image,
    model_name: str,
    quality: int,
    original_file_bytes: int,
) -> dict:
    """
    Pure synchronous inference — runs inside a ThreadPoolExecutor so it never
    blocks the FastAPI event loop.

    Alur:
      1. Convert PIL → tensor, pad to multiple-of-64
      2. model.compress()  → CompressAI bitstream  (akademis / BPP reference)
      3. model.decompress() → reconstructed tensor
      4. Crop padding, convert back to PIL
      5. Hitung PSNR & SSIM vs original
      6. Re-encode reconstructed → JPEG terkecil yang masih < ukuran file asli
         (resolusi TIDAK diturunkan)
    """
    t_start = time.perf_counter()
    log.info("[compressai] START model=%s quality=%d device=%s", model_name, quality, DEVICE)

    # ── 1. Prepare tensor ────────────────────────────────────────────────────
    original_np = np.array(img)
    x = transforms.ToTensor()(img).unsqueeze(0).to(DEVICE)  # [1, 3, H, W]
    x_padded, (h_orig, w_orig) = pad_image_tensor(x, multiple=64)
    log.info("[compressai] Image size: %dx%d (padded to %dx%d)",
             w_orig, h_orig, x_padded.shape[3], x_padded.shape[2])

    # ── 2. Load model (cached after first call) ───────────────────────────────
    model = get_model(model_name, quality)

    # ── 3. Encode → bitstream ─────────────────────────────────────────────────
    t_enc = time.perf_counter()
    with torch.no_grad():
        enc_out = model.compress(x_padded)
    log.info("[compressai] Encode done in %.2fs", time.perf_counter() - t_enc)

    bitstream_bytes = sum(len(s) for strings in enc_out["strings"] for s in strings)
    log.info("[compressai] Bitstream size: %d bytes", bitstream_bytes)

    # ── 4. Decode bitstream → reconstructed tensor ───────────────────────────
    t_dec = time.perf_counter()
    with torch.no_grad():
        dec_out = model.decompress(enc_out["strings"], enc_out["shape"])
    log.info("[compressai] Decode done in %.2fs", time.perf_counter() - t_dec)

    # ── 5. Post-process reconstructed image ──────────────────────────────────
    x_hat = dec_out["x_hat"].squeeze(0).clamp(0, 1).cpu()
    result_np = (x_hat.numpy().transpose(1, 2, 0) * 255).astype(np.uint8)
    result_np = result_np[:h_orig, :w_orig, :]          # crop padding artefacts
    result_img = Image.fromarray(result_np)

    # ── 6. Quality metrics (PSNR & SSIM — Table 1 of paper) ─────────────────
    metrics = calculate_metrics(original_np, result_np)
    bpp = (bitstream_bytes * 8) / max(h_orig * w_orig, 1)
    log.info("[compressai] PSNR=%.2f dB  SSIM=%.4f  BPP=%.4f",
             metrics["psnr"], metrics["ssim"], bpp)

    # ── 7. Re-encode → smallest JPEG < original file size ────────────────────
    output_jpeg_bytes = find_best_jpeg(result_img, original_file_bytes)
    output_file_bytes = len(output_jpeg_bytes)
    compression_ratio = round(original_file_bytes / max(output_file_bytes, 1), 2)
    log.info("[compressai] Output JPEG: %d bytes  ratio: %.2fx", output_file_bytes, compression_ratio)
    log.info("[compressai] TOTAL time: %.2fs", time.perf_counter() - t_start)

    return {
        "result": "data:image/jpeg;base64," + base64.b64encode(output_jpeg_bytes).decode(),
        "metrics": {
            **metrics,
            "bpp": round(bpp, 4),
            "original_bytes": original_file_bytes,    # ukuran file asli yang dikirim
            "compressed_bytes": output_file_bytes,    # ukuran JPEG output nyata
            "bitstream_bytes": bitstream_bytes,       # referensi akademis / BPP
            "compression_ratio": compression_ratio,
        },
        "model": model_name,
        "model_description": MODEL_REGISTRY[model_name]["description"],
        "paper_ref": MODEL_REGISTRY[model_name]["paper_ref"],
        "quality": quality,
        "device": DEVICE,
    }


@app.post("/compress-ai")
async def compress_ai(req: CompressAIRequest):
    """
    Deep learning image compression via CompressAI.
    Models correspond to papers reviewed in Yasin & Abdulazeez (2021).

    Heavy models (mbt2018, cheng2020_anchor) run in a ThreadPoolExecutor so
    the FastAPI event loop stays free and the client never receives a timeout
    while waiting for inference to finish.
    """
    if req.model not in MODEL_REGISTRY:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown model '{req.model}'. Available: {list(MODEL_REGISTRY.keys())}",
        )

    try:
        # Decode image and measure original file size on the event loop —
        # these are fast I/O ops, no need to offload them.
        img = decode_image(req.image)
        original_file_bytes = get_original_file_bytes(req.image)

        # Offload all blocking PyTorch work to the thread pool.
        # run_in_executor returns an awaitable; the event loop is free while
        # the worker thread runs model.compress / model.decompress.
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            _executor,
            _run_compressai_sync,
            img,
            req.model,
            req.quality,
            original_file_bytes,
        )
        return result

    except HTTPException:
        raise  # re-raise 400 from model validation above
    except torch.cuda.OutOfMemoryError:
        log.error("[compressai] GPU OOM")
        raise HTTPException(status_code=507, detail="GPU out of memory. Try a smaller image.")
    except MemoryError:
        log.error("[compressai] CPU OOM")
        raise HTTPException(status_code=507, detail="Out of memory. Try a smaller image.")
    except Exception as e:
        log.exception("[compressai] Unexpected error: %s", e)
        raise HTTPException(status_code=500, detail=f"CompressAI error: {str(e)}")