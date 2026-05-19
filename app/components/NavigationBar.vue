<script lang="ts" setup>
const { fileInput, openFilePicker, onFileChange } = useFilePicker();
</script>

<template>
  <!-- Added: fixed, top-0, w-full, z-50, and a backdrop blur effect -->
  <nav
    class="fixed top-0 w-full z-50 flex justify-between px-12.5 py-6.25 transition-all duration-300"
  >
    <nuxtLink to="/" class="font-semibold text-[24px] text-white">
      re<span class="text-brand">Minor</span>
    </nuxtLink>
    <div class="flex gap-7.5 items-center">
      <nuxtLink
        to="/compress"
        class="text-neutral-400 hover:text-white transition-colors"
        >I'm Feeling Lucky</nuxtLink
      >
      <nuxtLink to="/about" class="text-base hover:text-brand transition-colors"
        >About</nuxtLink
      >
      <button
        @click="openFilePicker"
        class="bg-tertiary text-primary font-medium p-2 rounded-base px-4 hover:bg-tertiary-dark border hover:border-tertiary-dark transition-all shadow-sm"
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
