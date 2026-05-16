<!-- index.vue -->
<script lang="ts" setup>
const showModal = ref(false);
const pendingFile = ref<File | null>(null);
</script>

<template>
  <div>
    <FeatureModal
      :show="showModal"
      :pendingFile="pendingFile"
      @close="showModal = false"
    />
  </div>
</template>
