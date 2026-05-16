let namespace = "compress";
export function useCompressor() {
  const {
    handleFile: baseHandleFile,
    loadFromSession: baseLoadFromSession,
    refresh,
    clear,
    sendToBackend,
  } = useUtils(namespace);
  const { preview, result, currentFile, loadFromStorage } = useImage(namespace);

  // tambah logic khusus compression di sini
  async function compress(quality: number = 80) {
    console.log("Compress berjalan");
    if (!currentFile.value) return;

    // logic sebelum kirim (kalau ada)

    await sendToBackend(currentFile.value, `/api/${namespace}`);

    // logic sesudah kirim (kalau ada)
  }

  async function handleFile(event: Event) {
    await baseHandleFile(event);
    await compress();
  }

  async function loadFromSession() {
    await baseLoadFromSession();
    await compress();
  }

  return {
    baseHandleFile,
    handleFile,
    compress,
    refresh,
    clear,
    loadFromSession,
    loadFromStorage,
    currentFile,
    preview,
    result,
  };
}
