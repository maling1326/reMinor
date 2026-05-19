<template>
  <div class="w-full flex-col justify-center mt-2 mx-2 p-2">
    <h1 class="text-6xl font-bold text-center">COMPRESS</h1>
    <div class="flex flex-col items-center justify-center">
      <label
        class="block mb-2.5 text-sm font-medium w-full text-center"
        for="file_input"
        >Upload file</label
      >
      <input
        id="file_input"
        type="file"
        accept="image/*"
        @change="handleFile"
        class="cursor-pointer border text-sm rounded-lg block w-min shadow-xs"
      />

      <div class="flex gap-2">
        <ClientOnly>
          <button
            @click="() => refresh()"
            :disabled="!currentFile"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded m-2"
          >
            Refresh
          </button>
          <button
            @click="() => compress()"
            :disabled="!currentFile"
            class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded m-2"
          >
            Compress
          </button>
        </ClientOnly>
        <button
          @click="() => clear()"
          class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded m-2"
        >
          Clear
        </button>
      </div>
    </div>

    <div
      v-if="preview || result"
      class="flex gap-4 items-center justify-center"
    >
      <div v-if="preview">
        <p class="font-bold text-4xl">Preview</p>
        <img :src="preview" alt="before" class="max-w-125 max-h-200" />
        <p>{{ formatSize(originalSize) }}</p>
      </div>
      <div v-if="result">
        <p class="font-bold text-4xl">Result</p>
        <img :src="result" alt="after" class="max-w-125 max-h-200" />
        <p>{{ formatSize(resultSize) }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
useHead({
  title: "Compress",
});

const {
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
} = useCompressor();

onMounted(async () => {
  const pending = sessionStorage.getItem("compress_pending");
  console.log(pending);

  if (pending) {
    await loadFromSession();
  } else {
    loadFromStorage();
  }

  window.addEventListener("dragdrop:newfile", async (e: Event) => {
    const { namespace } = (e as CustomEvent).detail;
    if (namespace !== "compress") return;
    await loadFromSession();
  });
});

onUnmounted(() => {
  window.removeEventListener("dragdrop:newfile", () => {});
});
</script>
