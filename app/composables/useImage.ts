export function useImage() {
  const preview = useState<string | null>("preview", () => null);
  const result = useState<string | null>("result", () => null);
  const currentFile = useState<File | null>("currentFile", () => null);

  function loadFromStorage() {
    preview.value = localStorage.getItem("preview");
    result.value = localStorage.getItem("result");
  }

  function clear() {
    preview.value = null;
    result.value = null;
    currentFile.value = null;
    localStorage.removeItem("preview");
    localStorage.removeItem("result");
  }

  return { preview, result, currentFile, loadFromStorage, clear };
}
