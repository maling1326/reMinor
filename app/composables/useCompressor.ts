export function useCompressor() {
  const { preview, result, currentFile } = useImage();

  async function sendToBackend(file: File) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/api/compress", {
      method: "POST",
      body: formData,
    });

    const blob = await response.blob();

    // Simpan result di localStorage
    const reader = new FileReader();
    reader.onload = () => {
      const base64 = reader.result as string;
      result.value = base64;
      localStorage.setItem("result", base64);
    };
    reader.readAsDataURL(blob);
  }

  async function handleFile(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;

    currentFile.value = file; // ← simpan filenya

    // Simpan preview di localStorage
    const reader = new FileReader();
    reader.onload = () => {
      const base64 = reader.result as string;
      preview.value = base64;
      localStorage.setItem("preview", base64);
    };
    reader.readAsDataURL(file);

    await sendToBackend(file); // ← pisah jadi function sendiri
  }

  async function refresh() {
    console.log("refresh clicked, currentFile:", currentFile.value);
    if (!currentFile.value) return;
    await sendToBackend(currentFile.value);
  }

  return { handleFile, refresh };
}
