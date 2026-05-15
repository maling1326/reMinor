export default defineEventHandler(async (event) => {
  if (event.method !== "POST") return;

  const formData = await readFormData(event);

  const response = await fetch("http://localhost:8000/compress", {
    method: "POST",
    body: formData,
  });

  const blob = await response.blob();
  const buffer = await blob.arrayBuffer();

  setHeader(event, "Content-Type", "image/jpeg");

  return Buffer.from(buffer);
});
