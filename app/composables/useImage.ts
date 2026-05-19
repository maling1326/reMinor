// useImage.ts
export function useImage(namespace: string = "default") {
  const preview = useState<string | null>(`${namespace}_preview`, () => null);
  const result = useState<string | null>(`${namespace}_result`, () => null);
  const currentFile = useState<File | null>(`${namespace}_file`, () => null);
  const originalSize = useState<number | null>(
    `${namespace}_originalSize`,
    () => null,
  );
  const resultSize = useState<number | null>(
    `${namespace}_resultSize`,
    () => null,
  );

  function loadFromStorage() {
    preview.value = localStorage.getItem(`${namespace}_preview`);
    result.value = localStorage.getItem(`${namespace}_result`);

    const savedOriginal = localStorage.getItem(`${namespace}_originalSize`);
    const savedResult = localStorage.getItem(`${namespace}_resultSize`);
    if (savedOriginal) originalSize.value = parseInt(savedOriginal);
    if (savedResult) resultSize.value = parseInt(savedResult);
  }

  return {
    preview,
    result,
    originalSize,
    resultSize,
    currentFile,
    loadFromStorage,
  };
}
