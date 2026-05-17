<script lang="ts" setup>
useHead({
  title: "Compress FIX",
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
  downloadResult,
} = useCompressor();

const { fileInput, openFilePicker, onFileChange } = useFilePicker();
</script>

<template>
  <MarginFeature>
    <div class="flex flex-col gap-12 w-full h-full">
      <h1 class="text-center w-full text-6xl font-extrabold">
        <span class="text-secondary">Compress</span> Image
      </h1>

      <!-- 3 Numbers -->
      <div v-if="preview && result" class="flex w-full justify-between">
        <!-- Before Compress -->
        <div
          class="w-90 h-fit max-h-min p-4 flex items-center bg-primary-light gap-5 rounded-base shadow-2xs shadow-secondary"
        >
          <img
            src="/assets/img/Jeffrey Epstein.jpg"
            alt="niba"
            class="max-h-20 object-cover"
          />
          <div class="flex flex-col gap-2">
            <h2 class="text-secondary! text-2xl">Before Compress</h2>
            <p class="text-3xl font-bold">{{ formatSize(originalSize) }}</p>
          </div>
        </div>

        <!-- Memory Saved -->
        <div
          class="w-90 h-fit max-h-min p-4 flex items-center bg-primary-light gap-5 rounded-base shadow-2xs shadow-secondary"
        >
          <img
            src="/assets/img/Jeffrey Epstein.jpg"
            alt="niba"
            class="max-h-20 object-cover"
          />
          <div class="flex flex-col gap-2">
            <h2 class="text-secondary! text-2xl">Memory Saved</h2>
            <p class="text-3xl font-bold">
              {{ formatSize(originalSize - resultSize) }}
            </p>
          </div>
        </div>

        <!-- After Compress -->
        <div
          class="w-90 h-fit max-h-min p-4 flex items-center bg-primary-light gap-5 rounded-base shadow-2xs shadow-secondary"
        >
          <img
            src="/assets/img/Jeffrey Epstein.jpg"
            alt="niba"
            class="max-h-20 object-cover"
          />
          <div class="flex flex-col gap-2">
            <h2 class="text-secondary! text-2xl">After Compress</h2>
            <p class="text-3xl font-bold">{{ formatSize(resultSize) }}</p>
          </div>
        </div>
      </div>

      <!-- Preview and Result -->
      <div
        v-if="preview && result"
        class="flex w-full h-full items-center justify-between border border-secondary/50 shadow-md shadow-secondary/75 bg-primary-light rounded-4xl overflow-hidden relative px-4 py-2"
      >
        <img
          :src="preview"
          alt="preview"
          class="max-h-140 flex w-full justify-center object-contain"
        />
        <img
          :src="result"
          alt="result"
          class="max-h-140 flex w-full justify-center object-contain"
        />

        <p
          class="absolute left-3 bg-base/10 backdrop-blur-lg rounded-2xl px-4 py-3 shadow-lg text-secondary! text-md"
        >
          Review
        </p>
        <p
          class="absolute right-3 bg-base/10 backdrop-blur-lg rounded-2xl px-4 py-3 shadow-lg text-secondary! text-md"
        >
          Result
        </p>
        <div
          class="absolute bottom-1 bg-base/10 backdrop-blur-lg rounded-2xl p-3 shadow-lg flex gap-4"
        >
          <button
            class="border border-secondary p-2 px-3 rounded-lg flex gap-2 justify-center items-center hover:bg-secondary/10 hover:cursor-pointer transition-all"
            @click="openFilePicker"
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 48 48"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <g clip-path="url(#clip0_986_877)">
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
                    opacity="0.5"
                    d="M39.457 21.8572C40.8824 27.195 39.5014 33.1266 35.3138 37.3142C29.0654 43.5626 18.9347 43.5626 12.6863 37.3142C6.4379 31.0658 6.4379 20.9352 12.6863 14.6868C18.9347 8.43839 29.0654 8.43839 35.3138 14.6868L36.728 16.101"
                    stroke="#FFDF90"
                    stroke-width="4"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                  <path
                    d="M28.2427 16.1005L36.7279 16.1005L36.7279 7.61523"
                    stroke="#FFDF90"
                    stroke-width="4"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </g>
              </g>
              <defs>
                <clipPath id="clip0_986_877">
                  <rect width="48" height="48" fill="white" />
                </clipPath>
              </defs>
            </svg>

            <p class="text-secondary!">Change Image</p>
          </button>
          <button
            class="border border-secondary p-2 px-3 rounded-lg flex gap-2 justify-center items-center bg-secondary hover:bg-secondary/80 hover:cursor-pointer transition-all"
            @click="downloadResult"
            :disabled="!result"
          >
            <svg
              width="24"
              height="24"
              viewBox="0 0 48 48"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                opacity="0.5"
                d="M41 14V26C41 33.5424 41 37.3138 38.6568 39.6568C36.3138 42 32.5424 42 25 42H23C15.4575 42 11.6863 42 9.34314 39.6568C7 37.3138 7 33.5424 7 26V14"
                stroke="#2B2B2B"
                stroke-width="5"
                stroke-linecap="round"
              />
              <path
                d="M4 10C4 8.11438 4 7.17158 4.58578 6.58578C5.17158 6 6.11438 6 8 6H40C41.8856 6 42.8284 6 43.4142 6.58578C44 7.17158 44 8.11438 44 10C44 11.8856 44 12.8284 43.4142 13.4142C42.8284 14 41.8856 14 40 14H8C6.11438 14 5.17158 14 4.58578 13.4142C4 12.8284 4 11.8856 4 10Z"
                stroke="#2B2B2B"
                stroke-width="5"
              />
              <path
                d="M24 14V32M18 25.3334L24 32L30 25.3334"
                stroke="#2B2B2B"
                stroke-width="5"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
            <p class="text-primary!">Download Result</p>
          </button>
        </div>
      </div>

      <!-- Box to add image -->
      <div
        v-if="!preview && !result"
        class="h-full bg-primary-light rounded-4xl border-dashed border-3 border-secondary/50 flex flex-col justify-center items-center hover:bg-secondary/10 transition-all ease-in-out duration-500 gap-4"
        @click="openFilePicker"
      >
        <svg
          width="36"
          height="36"
          viewBox="0 0 36 36"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <g clip-path="url(#clip0_982_865)">
            <path
              d="M29.025 15.06C28.005 9.885 23.46 6 18 6C13.665 6 9.9 8.46 8.025 12.06C3.51 12.54 6.78208e-09 16.365 5.55586e-09 21C4.24233e-09 25.965 4.035 30 9 30L28.5 30C32.64 30 36 26.64 36 22.5C36 18.54 32.925 15.33 29.025 15.06ZM28.5 27L9 27C5.685 27 3 24.315 3 21C3 17.925 5.295 15.36 8.34 15.045L9.945 14.88L10.695 13.455C12.12 10.71 14.91 9 18 9C21.93 9 25.32 11.79 26.085 15.645L26.535 17.895L28.83 18.06C31.17 18.21 33 20.175 33 22.5C33 24.975 30.975 27 28.5 27ZM12 19.5L15.825 19.5L15.825 24L20.175 24L20.175 19.5L24 19.5L18 13.5L12 19.5Z"
              fill="#FFDF90"
            />
          </g>
          <defs>
            <clipPath id="clip0_982_865">
              <rect width="36" height="36" fill="white" />
            </clipPath>
          </defs>
        </svg>
        <p>
          Drag your file or <span class="text-secondary font-bold">browse</span>
        </p>
        <p class="text-base/40!">*JPG, JPEG, or PNG</p>
      </div>
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        class="hidden"
        @change="handleFile"
      />
    </div>
  </MarginFeature>
</template>
