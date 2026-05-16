// useImage.ts
export function useImage(namespace: string = "default") {
  const preview = useState<string | null>(`${namespace}_preview`, () => null);
  const result = useState<string | null>(`${namespace}_result`, () => null);
  const currentFile = useState<File | null>(`${namespace}_file`, () => null);

  function loadFromStorage() {
    console.log("loadFromStorage Running");
    preview.value = localStorage.getItem(`${namespace}_preview`);
    result.value = localStorage.getItem(`${namespace}_result`);
  }

  return { preview, result, currentFile, loadFromStorage };
}
