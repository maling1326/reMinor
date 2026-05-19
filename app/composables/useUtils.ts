export function useUtils(namespace: string = "default") {
  const { preview, result, currentFile, originalSize, resultSize } =
    useImage(namespace);

  function readFileAsBase64(file: Blob): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }

  async function handleFile(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;

    currentFile.value = file;
    originalSize.value = file.size;
    localStorage.setItem(`${namespace}_originalSize`, file.size.toString());

    const base64 = await readFileAsBase64(file);
    preview.value = base64;
    localStorage.setItem(`${namespace}_preview`, base64);
  }

  async function sendToBackend(file: File, endpoint: string = "/api/compress") {
    const formData = new FormData();
    formData.append("file", file);
    const response = await fetch(endpoint, { method: "POST", body: formData });
    const blob = await response.blob();

    resultSize.value = blob.size;
    localStorage.setItem(`${namespace}_resultSize`, blob.size.toString());

    const base64 = await readFileAsBase64(blob as unknown as File);
    result.value = base64;
    localStorage.setItem(`${namespace}_result`, base64);
  }

  async function sendToBackendJSON(
    file: File,
    endpoint: string = "/api/compress",
    options: Record<string, unknown> = {},
  ) {
    const base64 = await readFileAsBase64(file);

    const response = await $fetch<{
      result: string;
      metrics?: {
        psnr?: number;
        ssim?: number;
        original_bytes?: number;
        compressed_bytes?: number;
        compression_ratio?: number;
        bpp?: number;
      };
    }>(endpoint, {
      method: "POST",
      body: { image: base64, ...options },
    });

    // Update result image
    result.value = response.result;
    localStorage.setItem(`${namespace}_result`, response.result);

    // Update result size dari metrics jika tersedia
    if (response.metrics?.compressed_bytes) {
      resultSize.value = response.metrics.compressed_bytes;
      localStorage.setItem(
        `${namespace}_resultSize`,
        response.metrics.compressed_bytes.toString(),
      );
    }

    return response; // return supaya caller bisa ambil metrics
  }

  async function refresh(endpoint: string = "/api/compress") {
    if (!currentFile.value) return;
    await sendToBackend(currentFile.value, endpoint);
  }

  // useUtils.ts
  async function loadFromSession() {
    const pending = sessionStorage.getItem(`${namespace}_pending`);
    if (!pending) return;

    preview.value = null;
    result.value = null;
    currentFile.value = null;

    const res = await fetch(pending);
    const blob = await res.blob();
    const file = new File([blob], "image.jpg", { type: blob.type });

    currentFile.value = file;
    originalSize.value = file.size;
    localStorage.setItem(`${namespace}_originalSize`, file.size.toString());

    preview.value = pending;
    localStorage.setItem(`${namespace}_preview`, pending);

    sessionStorage.removeItem(`${namespace}_pending`);
  }

  function clear() {
    preview.value = null;
    result.value = null;
    currentFile.value = null;
    originalSize.value = null;
    resultSize.value = null;
    localStorage.removeItem(`${namespace}_preview`);
    localStorage.removeItem(`${namespace}_result`);
    localStorage.removeItem(`${namespace}_originalSize`); // ← tambah
    localStorage.removeItem(`${namespace}_resultSize`); // ← tambah
  }

  function formatSize(bytes: number | null): string {
    if (!bytes) return "0 B";

    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
    if (bytes < 1024 * 1024 * 1000)
      return `${(bytes / 1024 / 1024).toFixed(2)} MB`;
    return `${(bytes / 1024 / 1024 / 1024).toFixed(2)} GB`;
  }

  function downloadResult() {
    if (!result.value) return;

    const a = document.createElement("a");
    a.href = result.value; // base64 string langsung bisa dipakai
    a.download = `compressed_${currentFile.value?.name ?? "image"}`;
    a.click();
  }

  return {
    handleFile, // <- Fungsi untuk menangani file yang di upload
    refresh, // <- Fungsi untuk mengirim ulang file ke backend
    clear, // <- Fungsi untuk menghapus data dari state dan localStorage
    sendToBackend, // <- Fungsi untuk mengirim file ke backend
    sendToBackendJSON,
    currentFile, // <- State untuk menyimpan file
    loadFromSession,
    formatSize,
    downloadResult,
  };
}
