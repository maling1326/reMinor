<script lang="ts" setup>
const fileInput = ref<HTMLInputElement | null>(null);

function openFilePicker() {
  fileInput.value?.click();
}

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  if (!file) return;

  // trigger event yang sama seperti di index
  // supaya DragDrop component bisa handle
  const dataTransfer = new DataTransfer();
  dataTransfer.items.add(file);

  window.dispatchEvent(
    new CustomEvent("filepicker:newfile", {
      detail: { file },
    }),
  );
}
</script>

<template>
  <nav class="flex justify-between px-12.5 py-6.25 bg-body">
    <nuxtLink to="/" class="font-semibold text-[24px] text-white">
      re<span class="text-brand">Minor</span>
    </nuxtLink>
    <div class="flex gap-7.5 items-center">
      <nuxtLink to="/" class="text-neutral-400">I'm Feeling Lucky</nuxtLink>
      <nuxtLink to="/about" class="text-base">About</nuxtLink>
      <button
        @click="openFilePicker"
        class="bg-tertiary p-2 rounded-base px-4 hover:bg-tertiary-dark border hover:border-tertiary-dark transition-all"
      >
        Tri Rianto Utomo
      </button>

      <!-- hidden input -->
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        class="hidden"
        @change="onFileChange"
      />
    </div>
  </nav>
</template>
