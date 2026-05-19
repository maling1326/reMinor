let namespace = "compress";
export function useCompressor() {
  const {
    handleFile: baseHandleFile,
    loadFromSession: baseLoadFromSession,
    refresh,
    clear,
    sendToBackend,
    formatSize,
    downloadResult,
  } = useUtils(namespace);
  const {
    preview,
    result,
    originalSize,
    resultSize,
    currentFile,
    loadFromStorage,
  } = useImage(namespace);

  // tambah logic khusus compression di sini
  async function compress(quality: number = 80) {
    console.log("Compress berjalan");
    if (!currentFile.value) return;

    await sendToBackend(currentFile.value, `/api/${namespace}`);
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
    formatSize,
    originalSize,
    resultSize,
    downloadResult,
  };
}
