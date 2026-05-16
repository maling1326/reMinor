<script lang="ts" setup>
const showModal = ref(false);
const pendingFile = ref<File | null>(null);

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  if (!file) return;
  pendingFile.value = file;
  showModal.value = true;
}
</script>

<template>
  <FeatureModal
    :show="showModal"
    :pendingFile="pendingFile"
    @close="showModal = false"
  />
  <div class="flex w-full justify-center my-28.75">
    <div class="flex flex-col gap-28.75 max-w-7xl w-full px-25">
      <div class="grid grid-cols-2 py-17.5 gap-20 items-stretch">
        <div class="w-full flex flex-col justify-between">
          <h1 class="font-bold text-6xl">
            Kompres <span class="font-black text-8xl text-brand">Lossless</span>
          </h1>

          <p class="text-[22px] text-base/65!">
            Kompresi ukuran citra tanpa mengubah resolusi atau kejernihan pixel
            menggunakan algoritma yang sudah teruji klinis.
          </p>

          <div>
            <button
              @click="openFilePicker"
              class="bg-secondary py-3 rounded-base px-4 hover:bg-secondary-dark border hover:border-secondary-dark transition-all text-[20px]"
            >
              Upload Gambar
            </button>

            <!-- hidden input -->
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              class="hidden"
              @change="onFileChange"
            />
            <p class="text-base/40! mt-1">*.JPG, *PNG, *JPEG</p>
          </div>
        </div>

        <div class="w-full flex justify-end items-center">
          <div
            class="p-4 rounded-base bg-secondary w-fit flex items-center justify-center"
          >
            <img
              src="~/assets/img/Jeffrey Epstein.jpg"
              alt="Tel Aviv"
              class="max-h-106.25 max-w-106.25 rounded-base object-contain"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
