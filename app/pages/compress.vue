<script lang="ts" setup>
useHead({ title: "Compress Image" });

// ── Composables ───────────────────────────────────────────────────────────────
const {
  baseHandleFile,
  loadFromSession,
  loadFromStorage,
  currentFile,
  preview,
  result,
  formatSize,
  originalSize,
  resultSize,
  downloadResult,
  clear,
} = useCompressor();

const {
  compressWithAI,
  isLoading,
  error,
  metrics,
  modelInfo,
  selectedModel,
  quality,
  qualityLabel,
  psnrRating,
  AI_MODELS,
} = useCompressorAI();

// ── Handler ───────────────────────────────────────────────────────────────────
async function handleNewFile(event: Event) {
  await baseHandleFile(event);
  await compressWithAI();
}

// ── Lifecycle ─────────────────────────────────────────────────────────────────
onMounted(async () => {
  const pending = sessionStorage.getItem("compress_pending");
  if (pending) {
    await loadFromSession();
    await compressWithAI();
  } else {
    loadFromStorage();
  }

  window.addEventListener("dragdrop:newfile", async (e: Event) => {
    const { namespace, file } = (e as CustomEvent).detail;
    if (namespace !== "compress") return;

    if (file) {
      const dt = new DataTransfer();
      dt.items.add(file);
      const input = document.createElement("input");
      input.files = dt.files;
      await handleNewFile({ target: input } as unknown as Event);
    } else {
      await loadFromSession();
      await compressWithAI();
    }
  });
});

onUnmounted(() => {
  window.removeEventListener("dragdrop:newfile", () => {});
});
</script>

<template>
  <MarginFeature>
    <!-- Removed redundant scroll container, relying on MarginFeature -->
    <div class="w-full flex flex-col gap-24 lg:gap-32 relative">
      <!-- Floating Loading indicator -->
      <div
        v-if="isLoading && !preview"
        class="fixed top-8 left-1/2 -translate-x-1/2 z-50 flex justify-center items-center gap-3 py-3 px-6 bg-primary-light/90 backdrop-blur-md border border-secondary/30 rounded-full shadow-lg shadow-black/50"
      >
        <div
          class="animate-spin w-5 h-5 border-2 border-secondary border-t-transparent rounded-full"
        />
        <p class="text-secondary font-medium text-sm">
          Compressing with deep learning...
        </p>
      </div>

      <!-- Floating Error -->
      <div
        v-if="error"
        class="fixed top-8 left-1/2 -translate-x-1/2 z-50 bg-red-900/90 backdrop-blur-md border border-red-400/50 rounded-xl px-6 py-3 text-red-100 text-sm shadow-lg shadow-black/50"
      >
        {{ error }}
      </div>

      <!-- ─────────────────────────────────────────────────────────────────── -->
      <!-- SECTION 1: Upload & Preview -->
      <!-- ─────────────────────────────────────────────────────────────────── -->
      <div
        class="min-h-[75vh] w-full snap-center flex flex-col justify-center items-center gap-8 mx-auto"
      >
        <h1 class="text-center w-full text-5xl md:text-6xl font-extrabold">
          <span class="text-secondary">Compress</span> Image
        </h1>

        <!-- Drop zone -->
        <label
          v-if="!preview && !result"
          class="w-full max-w-3xl aspect-[4/3] sm:aspect-video max-h-[400px] bg-primary-light rounded-[2rem] border-dashed border-2 border-secondary/50 flex flex-col justify-center items-center hover:bg-secondary/10 transition-all ease-in-out duration-300 gap-4 cursor-pointer group shadow-lg shadow-black/20"
          for="fileInput"
        >
          <div
            class="group-hover:scale-110 transition-transform duration-300"
            v-appear
          >
            <svg
              width="48"
              height="48"
              viewBox="0 0 36 36"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M29.025 15.06C28.005 9.885 23.46 6 18 6C13.665 6 9.9 8.46 8.025 12.06C3.51 12.54 6.78208e-09 16.365 5.55586e-09 21C4.24233e-09 25.965 4.035 30 9 30L28.5 30C32.64 30 36 26.64 36 22.5C36 18.54 32.925 15.33 29.025 15.06ZM28.5 27L9 27C5.685 27 3 24.315 3 21C3 17.925 5.295 15.36 8.34 15.045L9.945 14.88L10.695 13.455C12.12 10.71 14.91 9 18 9C21.93 9 25.32 11.79 26.085 15.645L26.535 17.895L28.83 18.06C31.17 18.21 33 20.175 33 22.5C33 24.975 30.975 27 28.5 27ZM12 19.5L15.825 19.5L15.825 24L20.175 24L20.175 19.5L24 19.5L18 13.5L12 19.5Z"
                fill="var(--color-secondary)"
              />
            </svg>
          </div>
          <p class="text-base text-center px-4" v-appear="200">
            Drag your file or
            <span class="text-secondary font-bold">browse</span>
          </p>
          <p class="text-sm text-white/40" v-appear="400">*JPG, JPEG, or PNG</p>
        </label>
        <input
          id="fileInput"
          type="file"
          accept="image/*"
          class="hidden"
          @change="handleNewFile"
        />

        <!-- 3 Size Numbers -->
        <div
          v-if="preview && result && !isLoading"
          class="grid grid-cols-1 sm:grid-cols-3 w-full gap-4 max-w-5xl"
        >
          <div
            class="w-full p-4 flex items-center justify-start bg-primary-light gap-4 rounded-2xl shadow-sm border border-transparent hover:border-secondary/30 hover:bg-black/20 hover:-translate-y-1 transition-all duration-300"
            v-appear
          >
            <svg
              width="48"
              height="48"
              viewBox="0 0 36 36"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              class="shrink-0"
            >
              <path
                d="M31 0C33.7614 1.28851e-07 36 2.23858 36 5V31C36 33.7614 33.7614 36 31 36H5C2.23858 36 1.28855e-07 33.7614 0 31V5C1.28855e-07 2.23858 2.23858 1.28851e-07 5 0H31ZM6.5 4.5C5.39543 4.5 4.5 5.39543 4.5 6.5V29.5C4.5 30.6046 5.39543 31.5 6.5 31.5H29.5C30.6046 31.5 31.5 30.6046 31.5 29.5V6.5C31.5 5.39543 30.6046 4.5 29.5 4.5H6.5Z"
                fill="var(--color-secondary)"
              />
              <path
                d="M28.3975 6H23.3975C22.569 6 21.8975 6.67157 21.8975 7.5C21.8975 8.32843 22.569 9 23.3975 9H28.3975C29.2259 9 29.8975 8.32843 29.8975 7.5C29.8975 6.67157 29.2259 6 28.3975 6Z"
                fill="var(--color-secondary)"
              />
              <path
                d="M29.8975 12.5V7.5C29.8975 6.67157 29.2259 6 28.3975 6C27.569 6 26.8975 6.67157 26.8975 7.5V12.5C26.8975 13.3284 27.569 14 28.3975 14C29.2259 14 29.8975 13.3284 29.8975 12.5Z"
                fill="var(--color-secondary)"
              />
              <path
                d="M25.0768 8.92169L21.1995 12.799C20.537 13.4615 20.537 14.5356 21.1995 15.198C21.862 15.8605 22.9361 15.8605 23.5985 15.198L27.4759 11.3207C28.1383 10.6582 28.1383 9.58417 27.4759 8.92169C26.8134 8.25922 25.7393 8.25922 25.0768 8.92169Z"
                fill="var(--color-secondary)"
              />
              <path
                d="M7.5 30H12.5C13.3284 30 14 29.3284 14 28.5C14 27.6716 13.3284 27 12.5 27H7.5C6.67157 27 6 27.6716 6 28.5C6 29.3284 6.67157 30 7.5 30Z"
                fill="var(--color-secondary)"
              />
              <path
                d="M6 23.5V28.5C6 29.3284 6.67157 30 7.5 30C8.32843 30 9 29.3284 9 28.5V23.5C9 22.6716 8.32843 22 7.5 22C6.67157 22 6 22.6716 6 23.5Z"
                fill="var(--color-secondary)"
              />
              <path
                d="M10.8206 27.0783L14.6979 23.201C15.3604 22.5385 15.3604 21.4644 14.6979 20.8019C14.0355 20.1395 12.9614 20.1395 12.2989 20.8019L8.42159 24.6793C7.75911 25.3418 7.75911 26.4158 8.42159 27.0783C9.08406 27.7408 10.1581 27.7408 10.8206 27.0783Z"
                fill="var(--color-secondary)"
              />
            </svg>
            <div class="flex flex-col gap-1 overflow-hidden">
              <h2
                class="text-secondary! text-sm font-semibold uppercase tracking-wider"
              >
                Before
              </h2>
              <p class="text-2xl font-bold truncate">
                {{ formatSize(originalSize) }}
              </p>
            </div>
          </div>

          <div
            class="w-full p-4 flex items-center justify-start bg-primary-light gap-4 rounded-2xl shadow-sm border border-transparent hover:border-secondary/30 hover:bg-black/20 hover:-translate-y-1 transition-all duration-300"
            v-appear="100"
          >
            <svg
              width="48"
              height="48"
              viewBox="0 0 42 40"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              class="shrink-0"
            >
              <path
                d="M22 0C32.4934 0 41 8.50659 41 19H20V0.0253906C20.3312 0.00821971 20.6646 5.14849e-10 21 0H22Z"
                fill="var(--color-secondary)"
              />
              <path
                d="M42.0029 21.0088C42.0029 27.0006 39.2279 32.3428 34.8945 35.8252L21.0059 21.0088H42.0029ZM21.0029 21.0059L21 21.0029L21.0029 21V21.0059Z"
                fill="var(--color-secondary)"
              />
              <path
                d="M18 20.9912L17.9971 20.9941L18 20.9971V21H18.0029L31.416 35.3086L31.8896 35.8164C28.6347 38.4326 24.5012 40 20 40H19C8.50659 40 0 31.4934 0 21C0 10.842 7.97142 2.54539 18 2.02539V20.9912Z"
                fill="var(--color-secondary)"
              />
            </svg>
            <div class="flex flex-col gap-1 overflow-hidden">
              <h2
                class="text-secondary! text-sm font-semibold uppercase tracking-wider"
              >
                Saved
              </h2>
              <p
                class="text-2xl font-bold truncate"
                :class="
                  (resultSize ?? 0) < (originalSize ?? 0)
                    ? 'text-green-400!'
                    : 'text-red-400!'
                "
              >
                {{ formatSize((originalSize ?? 0) - (resultSize ?? 0)) }}
              </p>
            </div>
          </div>

          <div
            class="w-full p-4 flex items-center justify-start bg-primary-light gap-4 rounded-2xl shadow-sm border border-transparent hover:border-secondary/30 hover:bg-black/20 hover:-translate-y-1 transition-all duration-300"
            v-appear="200"
          >
            <svg
              width="48"
              height="48"
              viewBox="0 0 36 36"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              class="shrink-0"
            >
              <path
                d="M31 0C33.7614 1.28851e-07 36 2.23858 36 5V31C36 33.7614 33.7614 36 31 36H5C2.23858 36 1.28855e-07 33.7614 0 31V5C1.28855e-07 2.23858 2.23858 1.28851e-07 5 0H31ZM6.5 4.5C5.39543 4.5 4.5 5.39543 4.5 6.5V29.5C4.5 30.6046 5.39543 31.5 6.5 31.5H29.5C30.6046 31.5 31.5 30.6046 31.5 29.5V6.5C31.5 5.39543 30.6046 4.5 29.5 4.5H6.5Z"
                fill="var(--color-secondary)"
              />
              <path
                d="M14.3975 20H9.39746C8.56903 20 7.89746 20.6716 7.89746 21.5C7.89746 22.3284 8.56903 23 9.39746 23H14.3975C15.2259 23 15.8975 22.3284 15.8975 21.5C15.8975 20.6716 15.2259 20 14.3975 20Z"
                fill="var(--color-secondary)"
              />
              <path
                d="M15.8975 26.5V21.5C15.8975 20.6716 15.2259 20 14.3975 20C13.569 20 12.8975 20.6716 12.8975 21.5V26.5C12.8975 27.3284 13.569 28 14.3975 28C15.2259 28 15.8975 27.3284 15.8975 26.5Z"
                fill="var(--color-secondary)"
              />
              <path
                d="M11.0768 22.9217L7.19951 26.799C6.53704 27.4615 6.53704 28.5356 7.19951 29.198C7.86199 29.8605 8.93607 29.8605 9.59854 29.198L13.4759 25.3207C14.1383 24.6582 14.1383 23.5842 13.4759 22.9217C12.8134 22.2592 11.7393 22.2592 11.0768 22.9217Z"
                fill="var(--color-secondary)"
              />
              <path
                d="M22.5 15.3975H27.5C28.3284 15.3975 29 14.7259 29 13.8975C29 13.069 28.3284 12.3975 27.5 12.3975H22.5C21.6716 12.3975 21 13.069 21 13.8975C21 14.7259 21.6716 15.3975 22.5 15.3975Z"
                fill="var(--color-secondary)"
              />
              <path
                d="M21 8.89746V13.8975C21 14.7259 21.6716 15.3975 22.5 15.3975C23.3284 15.3975 24 14.7259 24 13.8975V8.89746C24 8.06903 23.3284 7.39746 22.5 7.39746C21.6716 7.39746 21 8.06903 21 8.89746Z"
                fill="var(--color-secondary)"
              />
              <path
                d="M25.8206 12.4758L29.6979 8.59844C30.3604 7.93597 30.3604 6.86188 29.6979 6.19941C29.0355 5.53694 27.9614 5.53694 27.2989 6.19941L23.4216 10.0767C22.7591 10.7392 22.7591 11.8133 23.4216 12.4758C24.0841 13.1382 25.1581 13.1382 25.8206 12.4758Z"
                fill="var(--color-secondary)"
              />
            </svg>
            <div class="flex flex-col gap-1 overflow-hidden">
              <h2
                class="text-secondary! text-sm font-semibold uppercase tracking-wider"
              >
                After
              </h2>
              <p class="text-2xl font-bold truncate">
                {{ formatSize(resultSize) }}
              </p>
            </div>
          </div>
        </div>

        <!-- Preview and Result Container -->
        <div
          v-if="preview && result && !isLoading"
          class="flex flex-col lg:flex-row w-full flex-1 min-h-[350px] max-h-[600px] border border-secondary/30 shadow-xl shadow-black/40 bg-primary-light rounded-[2rem] overflow-hidden relative p-4 lg:p-6 gap-6 items-center justify-center max-w-5xl"
        >
          <!-- Preview -->
          <div
            class="w-full h-1/2 lg:h-full lg:w-1/2 flex justify-center items-center rounded-xl bg-primary/30 overflow-hidden relative border border-transparent hover:border-secondary/20 transition-all"
            v-appear="100"
          >
            <p
              class="absolute top-4 left-4 bg-primary/60 backdrop-blur-md rounded-xl px-4 py-2 shadow-lg text-secondary! text-sm font-bold z-10"
              v-appear="500"
            >
              Original
            </p>
            <img
              :src="preview"
              alt="preview"
              class="w-full h-full object-contain p-2 hover:scale-[1.02] transition-transform duration-500 ease-in-out"
            />
          </div>

          <!-- Result -->
          <div
            class="w-full h-1/2 lg:h-full lg:w-1/2 flex justify-center items-center rounded-xl bg-primary/30 overflow-hidden relative border border-transparent hover:border-secondary/20 transition-all"
            v-appear="200"
          >
            <p
              class="absolute top-4 right-4 bg-primary/60 backdrop-blur-md rounded-xl px-4 py-2 shadow-lg text-secondary! text-sm font-bold z-10"
              v-appear="500"
            >
              Compressed
            </p>
            <img
              :src="result"
              alt="result"
              class="w-full h-full object-contain p-2 hover:scale-[1.02] transition-transform duration-500 ease-in-out"
            />
          </div>

          <!-- Bottom controls (Absolute overlay over images) -->
          <div
            class="absolute bottom-6 left-1/2 -translate-x-1/2 flex justify-center items-center w-[90%] md:w-auto"
          >
            <div
              class="bg-primary/80 backdrop-blur-xl border border-secondary/20 rounded-2xl p-2 md:p-3 shadow-xl flex flex-wrap justify-center gap-2 md:gap-4"
            >
              <label
                class="border border-secondary/70 px-4 py-2 rounded-xl flex gap-2 justify-center items-center hover:bg-secondary/20 hover:cursor-pointer transition-all"
                for="ChangeImage"
              >
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 48 48"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <mask
                    id="mask0_986_877"
                    style="mask-type: luminance"
                    maskUnits="userSpaceOnUse"
                    x="0"
                    y="0"
                    width="48"
                    height="48"
                  >
                    <path
                      d="M48 1.26988e-08L1.26988e-08 0L0 48L48 48L48 1.26988e-08Z"
                      fill="white"
                    />
                  </mask>
                  <g mask="url(#mask0_986_877)">
                    <path
                      opacity="0.8"
                      d="M39.457 21.8572C40.8824 27.195 39.5014 33.1266 35.3138 37.3142C29.0654 43.5626 18.9347 43.5626 12.6863 37.3142C6.4379 31.0658 6.4379 20.9352 12.6863 14.6868C18.9347 8.43839 29.0654 8.43839 35.3138 14.6868L36.728 16.101"
                      stroke="var(--color-secondary)"
                      stroke-width="4"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                    <path
                      d="M28.2427 16.1005L36.7279 16.1005L36.7279 7.61523"
                      stroke="var(--color-secondary)"
                      stroke-width="4"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </g>
                </svg>
                <span class="text-secondary! text-sm font-medium"
                  >Change Image</span
                >
              </label>
              <input
                id="ChangeImage"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleNewFile"
              />

              <button
                class="border border-secondary px-4 py-2 rounded-xl flex gap-2 justify-center items-center bg-secondary hover:bg-secondary/80 transition-all disabled:opacity-50 hover:cursor-pointer"
                @click="downloadResult"
                :disabled="!result"
              >
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 48 48"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    opacity="0.8"
                    d="M41 14V26C41 33.5424 41 37.3138 38.6568 39.6568C36.3138 42 32.5424 42 25 42H23C15.4575 42 11.6863 42 9.34314 39.6568C7 37.3138 7 33.5424 7 26V14"
                    stroke="var(--color-primary)"
                    stroke-width="5"
                    stroke-linecap="round"
                  />
                  <path
                    d="M4 10C4 8.11438 4 7.17158 4.58578 6.58578C5.17158 6 6.11438 6 8 6H40C41.8856 6 42.8284 6 43.4142 6.58578C44 7.17158 44 8.11438 44 10C44 11.8856 44 12.8284 43.4142 13.4142C42.8284 14 41.8856 14 40 14H8C6.11438 14 5.17158 14 4.58578 13.4142C4 12.8284 4 11.8856 4 10Z"
                    stroke="var(--color-primary)"
                    stroke-width="5"
                  />
                  <path
                    d="M24 14V32M18 25.3334L24 32L30 25.3334"
                    stroke="var(--color-primary)"
                    stroke-width="5"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
                <span class="text-primary! text-sm font-bold">Download</span>
              </button>

              <button
                class="border border-white/10 px-4 py-2 rounded-xl flex gap-2 justify-center items-center hover:bg-red-900/30 hover:border-red-400/50 hover:cursor-pointer transition-all"
                @click="clear"
              >
                <span
                  class="text-white/60 text-sm font-medium hover:text-red-300"
                  >Clear</span
                >
              </button>
            </div>
          </div>
        </div>

        <!-- Loading placeholder -->
        <div
          v-if="preview && isLoading"
          class="flex flex-col w-full flex-1 min-h-[350px] max-h-[600px] items-center justify-center border-2 border-dashed border-secondary/30 bg-primary-light/50 rounded-[2rem] max-w-5xl p-6"
        >
          <div class="flex flex-col items-center gap-6">
            <div
              class="animate-spin w-12 h-12 border-4 border-secondary border-t-transparent rounded-full shadow-lg"
            />
            <div class="text-center">
              <p class="text-secondary text-xl font-bold mb-1">
                Running deep learning model...
              </p>
              <p class="text-white/40 text-sm">
                First run will download model weights (~30MB)
              </p>
            </div>
          </div>
        </div>

        <!-- Scroll Prompt indicator -->
        <div
          v-if="metrics && !isLoading && preview && result"
          class="hidden md:flex flex-col items-center opacity-60 animate-bounce mt-4"
        >
          <p class="text-xs text-white/50 mb-1">Scroll for settings</p>
          <svg
            class="w-5 h-5 text-secondary"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 14l-7 7m0 0l-7-7m7 7V3"
            ></path>
          </svg>
        </div>
      </div>

      <!-- ─────────────────────────────────────────────────────────────────── -->
      <!-- SECTION 2: Settings & Metrics -->
      <!-- ─────────────────────────────────────────────────────────────────── -->
      <div
        v-if="metrics && !isLoading && preview && result"
        class="min-h-[75vh] w-full snap-center flex flex-col justify-center items-center gap-12 mx-auto"
      >
        <h1 class="text-center w-full text-5xl md:text-6xl font-extrabold">
          <span class="text-tertiary">Compression</span> Settings
        </h1>

        <!-- Model & Quality selector -->
        <div
          v-if="preview"
          class="w-full flex flex-wrap gap-6 justify-between items-end bg-primary-light rounded-3xl p-6 md:p-8 border border-tertiary/20 shadow-xl shadow-black/20 max-w-5xl"
          v-appear
        >
          <div class="flex flex-col gap-2 flex-1 min-w-[200px]">
            <label
              class="text-tertiary! font-bold text-sm tracking-wide uppercase"
              >AI Model</label
            >
            <select
              v-model="selectedModel"
              class="bg-primary border border-tertiary/30 rounded-xl px-4 py-3 text-base text-white cursor-pointer focus:outline-none focus:border-tertiary transition-colors"
            >
              <option v-for="(info, key) in AI_MODELS" :key="key" :value="key">
                {{ info.label }} — {{ info.ref }}
              </option>
            </select>
            <p class="text-xs text-white/40 mt-1">
              {{ AI_MODELS[selectedModel].desc }}
            </p>
          </div>

          <div class="flex flex-col gap-2 flex-1 min-w-[200px] mb-[1.25rem]">
            <label
              class="text-tertiary! font-bold text-sm tracking-wide uppercase flex justify-between"
            >
              <span
                >Quality
                <span class="text-white/50 font-normal normal-case"
                  >({{ qualityLabel }})</span
                ></span
              >
              <span class="text-white/80"
                >{{ quality }} / {{ AI_MODELS[selectedModel].maxQuality }}</span
              >
            </label>
            <input
              v-model.number="quality"
              type="range"
              :min="1"
              :max="AI_MODELS[selectedModel].maxQuality"
              step="1"
              class="accent-tertiary w-full h-2 bg-primary rounded-lg appearance-none cursor-pointer mt-2"
            />
          </div>

          <button
            @click="compressWithAI()"
            :disabled="isLoading || !currentFile"
            class="border border-tertiary px-8 py-3 rounded-xl bg-tertiary text-primary text-base font-bold hover:bg-tertiary/80 transition-all disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap mb-[1.25rem] shadow-lg shadow-tertiary/20"
          >
            {{ isLoading ? "Processing..." : "Re-compress" }}
          </button>
        </div>

        <!-- Metrics Data Grid -->
        <div
          v-if="metrics && !isLoading && preview && result"
          class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 w-full max-w-5xl"
        >
          <div
            class="bg-primary-light rounded-2xl p-5 border border-tertiary/20 flex flex-col items-center justify-center gap-2 hover:bg-tertiary/5 transition-colors shadow-sm"
            v-appear="200"
          >
            <p class="text-xs text-white/50 uppercase tracking-widest">
              PSNR (dB)
            </p>
            <p
              class="text-3xl font-bold"
              :class="psnrRating?.color ?? 'text-white'"
            >
              {{ metrics.psnr }}
            </p>
            <p class="text-xs font-medium" :class="psnrRating?.color ?? ''">
              {{ psnrRating?.label }}
            </p>
          </div>

          <div
            class="bg-primary-light rounded-2xl p-5 border border-tertiary/20 flex flex-col items-center justify-center gap-2 hover:bg-tertiary/5 transition-colors shadow-sm"
            v-appear="300"
          >
            <p class="text-xs text-white/50 uppercase tracking-widest">SSIM</p>
            <p class="text-3xl font-bold text-blue-400">{{ metrics.ssim }}</p>
            <p class="text-xs text-white/40">Max 1.0</p>
          </div>

          <div
            class="bg-primary-light rounded-2xl p-5 border border-tertiary/20 flex flex-col items-center justify-center gap-2 hover:bg-tertiary/5 transition-colors shadow-sm"
            v-appear="400"
          >
            <p class="text-xs text-white/50 uppercase tracking-widest">BPP</p>
            <p class="text-3xl font-bold text-purple-400">{{ metrics.bpp }}</p>
            <p class="text-xs text-white/40">Bits per pixel</p>
          </div>

          <div
            class="bg-primary-light rounded-2xl p-5 border border-tertiary/20 flex flex-col items-center justify-center gap-2 hover:bg-tertiary/5 transition-colors shadow-sm"
            v-appear="500"
          >
            <p class="text-xs text-white/50 uppercase tracking-widest">Ratio</p>
            <p class="text-3xl font-bold text-green-400">
              {{ metrics.compression_ratio }}x
            </p>
            <p class="text-xs text-white/40">Compression factor</p>
          </div>

          <div
            v-if="metrics?.bitstream_bytes"
            class="bg-primary-light rounded-2xl p-5 border border-tertiary/20 flex flex-col items-center justify-center gap-2 hover:bg-tertiary/5 transition-colors shadow-sm col-span-2 md:col-span-1 lg:col-span-1"
            v-appear="600"
          >
            <p class="text-xs text-white/50 uppercase tracking-widest">
              Bitstream
            </p>
            <p class="text-3xl font-bold text-yellow-400">
              {{ formatSize(metrics.bitstream_bytes) }}
            </p>
            <p class="text-xs text-white/40">Internal size</p>
          </div>
        </div>

        <!-- Model Info Detail Box -->
        <div
          v-if="modelInfo"
          class="w-full max-w-5xl bg-primary/40 border border-white/5 rounded-2xl p-6 text-center shadow-inner"
          v-appear="800"
        >
          <p class="text-sm text-tertiary font-bold mb-2">
            Model: {{ modelInfo.description }}
          </p>
          <div
            class="flex flex-col sm:flex-row justify-center items-center gap-4 sm:gap-8 text-xs text-white/40"
          >
            <p>
              Paper Reference:
              <span class="text-white/60">{{ modelInfo.paper_ref }}</span>
            </p>
            <p class="hidden sm:block">•</p>
            <p>
              Execution Device:
              <span class="text-white/60 uppercase tracking-widest">{{
                modelInfo.device
              }}</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  </MarginFeature>
</template>
