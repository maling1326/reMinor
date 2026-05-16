<!-- index.vue -->
<script lang="ts" setup>
const showModal = ref(false);

// saat file dipilih, tampilkan modal
function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement;
  if (!input.files?.[0]) return;

  // simpan file sementara di sessionStorage biar tidak hilang saat redirect
  const reader = new FileReader();
  reader.onload = () => {
    sessionStorage.setItem("pending_file", reader.result as string);
  };
  reader.readAsDataURL(input.files[0]);

  showModal.value = true; // tampilkan modal
}

function selectFeature(path: string) {
  showModal.value = false;
  navigateTo(path); // redirect ke halaman fitur
}
</script>

<template>
  <div>
    <input type="file" accept="image/*" @change="onFileChange" />

    <!-- Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <div
        class="bg-white rounded-xl p-8 grid grid-cols-2 gap-4 max-w-md w-full"
      >
        <h2 class="col-span-2 text-xl font-bold text-center">Pilih Fitur</h2>

        <button
          v-for="feature in features"
          :key="feature.path"
          @click="selectFeature(feature.path)"
          class="border-2 rounded-lg p-4 hover:bg-blue-50 hover:border-blue-500 transition"
        >
          {{ feature.label }}
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
const features = [
  { label: "Compress", path: "/compress" },
  { label: "Fitur 2", path: "/compress" },
  { label: "Fitur 3", path: "/compress" },
  { label: "Fitur 4", path: "/compress" },
  { label: "Fitur 5", path: "/compress" },
  { label: "Fitur 6", path: "/compress" },
];
</script>
