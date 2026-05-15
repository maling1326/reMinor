<template>
  <div>
    <input type="file" accept="image/*" @change="handleFile" />
    <button
      @click="refresh"
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded m-2"
    >
      Refresh
    </button>
    <button
      @click="clear"
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded m-2"
    >
      Clear
    </button>

    <div v-if="preview && result" class="flex gap-4">
      <div>
        <img :src="preview" alt="before" class="max-w-125 max-h-200" />
        <p class="font-md">{{ currentFile?.size }} bytes</p>
      </div>
      <div>
        <img :src="result" alt="after" class="max-w-125 max-h-200" />
        <!-- <p class="font-md">{{ result?.size }}</p> -->
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
const { preview, result, currentFile, loadFromStorage, clear } = useImage();
const { handleFile, refresh } = useCompressor();

onMounted(() => {
  loadFromStorage();
});
</script>
