export function useUtils(namespace: string = "default") {
  const { preview, result, currentFile, originalSize, resultSize } =
    useImage(namespace);

  // useUtils.ts
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

    const base64 = await readFileAsBase64(blob as unknown as File);
    result.value = base64;
    localStorage.setItem(`${namespace}_result`, base64);
  }

  async function refresh(endpoint: string = "/api/compress") {
    if (!currentFile.value) return;
    await sendToBackend(currentFile.value, endpoint);
  }

  // useUtils.ts
  async function loadFromSession() {
    const pending = sessionStorage.getItem(`${namespace}_pending`);
    if (!pending) return;

    // clear state lama dulu ✅
    preview.value = null;
    result.value = null;
    currentFile.value = null;

    // baru set yang baru
    const res = await fetch(pending);
    const blob = await res.blob();
    const file = new File([blob], "image.jpg", { type: blob.type });

    currentFile.value = file;
    preview.value = pending;
    localStorage.setItem(`${namespace}_preview`, pending);

    sessionStorage.removeItem(`${namespace}_pending`);
  }

  function clear() {
    preview.value = null;
    result.value = null;
    currentFile.value = null;
    localStorage.removeItem(`${namespace}_preview`);
    localStorage.removeItem(`${namespace}_result`);
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
    currentFile, // <- State untuk menyimpan file
    loadFromSession,
    formatSize,
    downloadResult,
  };
}
