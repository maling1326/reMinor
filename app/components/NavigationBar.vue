<script lang="ts" setup>
const { fileInput, openFilePicker, onFileChange } = useFilePicker();
</script>

<template>
  <nav class="flex justify-between px-12.5 py-6.25 bg-body">
    <nuxtLink to="/" class="font-semibold text-[24px] text-white">
      re<span class="text-brand">Minor</span>
    </nuxtLink>
    <div class="flex gap-7.5 items-center">
      <nuxtLink to="/compress" class="text-neutral-400"
        >I'm Feeling Lucky</nuxtLink
      >
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
