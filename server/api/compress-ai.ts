// server/api/compress-ai.ts
// Nuxt proxy → FastAPI /compress-ai

// Heavy models (mbt2018, cheng2020_anchor) can take several minutes on CPU.
// NODE_TIMEOUT_MS lets you override per-environment via .env if needed.
const TIMEOUT_MS = Number(process.env.NODE_TIMEOUT_MS ?? 10 * 60 * 1000); // default 10 min

export default defineEventHandler(async (event) => {
  const body = await readBody(event);

  // AbortController lets us cancel the fetch cleanly when the timeout fires,
  // so the socket to FastAPI is properly closed rather than left dangling.
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

  let response: Response;

  try {
    response = await fetch("http://localhost:8000/compress-ai", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      signal: controller.signal,
    });
  } catch (err: unknown) {
    // AbortError = our timeout fired; any other error = FastAPI unreachable
    const isTimeout = err instanceof Error && err.name === "AbortError";
    throw createError({
      statusCode: isTimeout ? 504 : 502,
      statusMessage: isTimeout
        ? `Inference timed out after ${TIMEOUT_MS / 1000}s. Try a smaller image or lower quality.`
        : "Could not reach the compression backend. Is FastAPI running?",
    });
  } finally {
    clearTimeout(timer); // always clean up, even on success
  }

  if (!response.ok) {
    // Forward FastAPI's own error detail (e.g. "GPU OOM", "Unknown model")
    const error = await response
      .json()
      .catch(() => ({ detail: "Unknown error from backend" }));
    throw createError({
      statusCode: response.status,
      statusMessage: error.detail ?? "CompressAI error",
    });
  }

  return response.json();
});
