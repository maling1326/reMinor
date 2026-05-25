// composables/useCompressorAI.ts
// Fixed: aligned with useImage (result, currentFile — bukan resultImage/image)

export type CompressAIModel =
  | "bmshj2018_factorized"
  | "bmshj2018_hyperprior"
  | "mbt2018"
  | "cheng2020_anchor";

export interface CompressAIMetrics {
  psnr: number;
  ssim: number;
  bpp: number;
  original_bytes: number;
  compressed_bytes: number;
  compression_ratio: number;
}

export interface CompressAIResult {
  result: string;
  metrics: CompressAIMetrics;
  model: string;
  model_description: string;
  paper_ref: string;
  quality: number;
  device: string;
}

export const AI_MODELS: Record<
  CompressAIModel,
  { label: string; desc: string; ref: string; maxQuality: number }
> = {
  bmshj2018_factorized: {
    label: "Factorized CNN",
    desc: "Lightweight CNN end-to-end compression",
    ref: "CNN end-to-end",
    maxQuality: 8,
  },
  bmshj2018_hyperprior: {
    label: "Hyperprior CNN",
    desc: "CNN with hyperprior entropy model",
    ref: "CNN end-to-end",
    maxQuality: 8,
  },
  mbt2018: {
    label: "Tiled Deep Network",
    desc: "Spatially adaptive — Minnen et al. (Ref [76])",
    ref: "Ref [76] in paper",
    maxQuality: 8,
  },
  cheng2020_anchor: {
    label: "Deep Conv. Autoencoder",
    desc: "Best quality — Cheng et al. (Ref [74])",
    ref: "Ref [74] in paper",
    maxQuality: 6,
  },
};

export function useCompressorAI() {
  // Gunakan useImage & useUtils dengan namespace "compress"
  // agar state shared dengan useCompressor
  const { result, currentFile, resultSize } = useImage("compress");
  const { sendToBackendJSON } = useUtils("compress");

  const isLoading = ref(false);
  const error = ref<string | null>(null);
  const metrics = ref<CompressAIMetrics | null>(null);
  const modelInfo = ref<{
    model: string;
    description: string;
    paper_ref: string;
    device: string;
  } | null>(null);

  const selectedModel = ref<CompressAIModel>("bmshj2018_factorized");
  const quality = ref(3); // 1–8

  // Clamp quality whenever the model changes so the UI never shows a value
  // the backend silently overrides (cheng2020_anchor tops out at 6, not 8).
  watch(selectedModel, (model) => {
    const max = AI_MODELS[model].maxQuality;
    if (quality.value > max) quality.value = max;
  });

  async function compressWithAI(file?: File) {
    // Pakai file yang dipass, atau ambil dari state currentFile
    const target = file ?? currentFile.value;
    if (!target) {
      error.value = "No image selected";
      return;
    }

    isLoading.value = true;
    error.value = null;
    metrics.value = null;

    try {
      // sendToBackendJSON sudah handle update result & resultSize di useUtils
      const response = (await sendToBackendJSON(target, "/api/compress-ai", {
        quality: quality.value,
        model: selectedModel.value,
      })) as CompressAIResult;

      metrics.value = response.metrics;
      modelInfo.value = {
        model: response.model,
        description: response.model_description,
        paper_ref: response.paper_ref,
        device: response.device,
      };
    } catch (err: unknown) {
      const e = err as {
        data?: { statusMessage?: string };
        message?: string;
        statusCode?: number;
      };
      // 504 = timeout from our proxy — give a more actionable message
      if (e?.statusCode === 504) {
        error.value =
          "Inference timed out. Try a smaller image or lower quality level.";
      } else {
        error.value =
          e?.data?.statusMessage ?? e?.message ?? "Compression failed";
      }
    } finally {
      isLoading.value = false;
    }
  }

  // Quality label untuk UI
  const qualityLabel = computed(() => {
    const q = quality.value;
    if (q <= 2) return "Low (fastest)";
    if (q <= 4) return "Medium";
    if (q <= 6) return "High";
    return "Ultra (slowest)";
  });

  // Rating PSNR sesuai range di Table 1 paper
  const psnrRating = computed(() => {
    if (!metrics.value) return null;
    const p = metrics.value.psnr;
    if (p >= 40) return { label: "Excellent", color: "text-green-500" };
    if (p >= 35) return { label: "Good", color: "text-blue-500" };
    if (p >= 30) return { label: "Acceptable", color: "text-yellow-500" };
    return { label: "Low", color: "text-red-500" };
  });

  return {
    // State
    isLoading,
    error,
    metrics,
    modelInfo,
    selectedModel,
    quality,
    qualityLabel,
    psnrRating,
    // Shared image state (dari useImage)
    result,
    currentFile,
    resultSize,
    // Actions
    compressWithAI,
    // Constants
    AI_MODELS,
  };
}
