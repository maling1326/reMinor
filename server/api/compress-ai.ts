// server/api/compress-ai.ts
// Nuxt proxy → FastAPI /compress-ai

export default defineEventHandler(async (event) => {
  const body = await readBody(event);

  const response = await fetch("http://localhost:8000/compress-ai", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const error = await response
      .json()
      .catch(() => ({ detail: "Unknown error" }));
    throw createError({
      statusCode: response.status,
      statusMessage: error.detail ?? "CompressAI error",
    });
  }

  return response.json();
});
