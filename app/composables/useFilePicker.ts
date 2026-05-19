export function useFilePicker() {
  const fileInput = ref<HTMLInputElement | null>(null);

  function openFilePicker() {
    fileInput.value?.click();
  }

  function onFileChange(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;

    window.dispatchEvent(
      new CustomEvent("filepicker:newfile", {
        detail: { file },
      }),
    );

    input.value = "";
  }

  return { fileInput, openFilePicker, onFileChange };
}
