<script lang="ts" setup>
const isDragging = ref(false);
const showModal = ref(false);
const pendingFile = ref<File | null>(null);

const route = useRoute();

const featureRoutes = [
  "/compress",
  "/convert",
  "/resize",
  "/adjust",
  "/minor",
  "/major",
];

const features = [
  { label: "Compress", path: "/compress", namespace: "compress" },
  { label: "Convert", path: "/compress", namespace: "compress" },
  { label: "Resize", path: "/compress", namespace: "compress" },
  { label: "Adjust", path: "/compress", namespace: "compress" },
  { label: "minor", path: "/compress", namespace: "compress" },
  { label: "major", path: "/compress", namespace: "compress" },
];

// ================================
// Cek apakah halaman sekarang adalah feature page
// ================================
const isFeaturePage = computed(() => featureRoutes.includes(route.path));

// ================================
// Drag and Drop
// ================================
function onDragEnter(e: DragEvent) {
  e.preventDefault();
  isDragging.value = true;
}

function onDragLeave(e: DragEvent) {
  if (e.relatedTarget === null) {
    isDragging.value = false;
  }
}

function onDragOver(e: DragEvent) {
  e.preventDefault();
}

async function onDrop(e: DragEvent) {
  e.preventDefault();
  isDragging.value = false;

  const file = e.dataTransfer?.files[0];
  if (!file) return;
  if (!file.type.startsWith("image/")) return;

  pendingFile.value = file;

  if (isFeaturePage.value) {
    // langsung update gambar di halaman fitur yang sedang dibuka
    await loadToCurrentPage();
  } else {
    // tampilkan modal pilih fitur
    showModal.value = true;
  }
}

// ================================
// Load ke halaman fitur yang sedang dibuka
// ================================
async function loadToCurrentPage() {
  if (!pendingFile.value) return;

  // cari namespace berdasarkan route sekarang
  const feature = features.find((f) => f.path === route.path);
  if (!feature) return;

  const reader = new FileReader();
  const base64 = await new Promise<string>((resolve, reject) => {
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = reject;
    reader.readAsDataURL(pendingFile.value!);
  });

  // simpan ke sessionStorage dengan namespace yang sesuai
  sessionStorage.setItem(`${feature.namespace}_pending`, base64);

  // trigger loadFromSession di halaman sekarang
  // pakai event supaya halaman bisa listen
  window.dispatchEvent(
    new CustomEvent("dragdrop:newfile", {
      detail: { namespace: feature.namespace },
    }),
  );
}

// ================================
// Pilih Fitur (dari modal)
// ================================
async function selectFeatures(path: string, namespace: string) {
  if (!pendingFile.value) return;

  const reader = new FileReader();
  const base64 = await new Promise<string>((resolve, reject) => {
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = reject;
    reader.readAsDataURL(pendingFile.value!);
  });

  sessionStorage.setItem(`${namespace}_pending`, base64);
  showModal.value = false;
  await navigateTo(path);
}
</script>

<template>
  <div
    class="min-h-screen"
    @dragenter="onDragEnter"
    @dragleave="onDragLeave"
    @dragover="onDragOver"
    @drop="onDrop"
  >
    <!-- Drag Overlay -->
    <Transition name="fade">
      <div
        v-if="isDragging"
        class="fixed inset-0 bg-blue-500/30 border-4 border-dashed border-blue-500 z-50 flex items-center justify-center pointer-events-none"
      >
        <p class="text-blue-700 text-4xl font-bold">Drop gambar di sini!</p>
      </div>
    </Transition>

    <!-- Modal Pilih Fitur -->
    <Transition name="fade">
      <div
        v-if="showModal"
        class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      >
        <div
          class="bg-white grid grid-cols-2 rounded-xl gap-4 max-w-md w-full p-4"
        >
          <p class="col-span-2 text-xl text-center font-bold">Pilih Fitur</p>
          <button
            v-for="feature in features"
            :key="feature.path"
            @click="selectFeatures(feature.path, feature.namespace)"
            class="rounded-md border border-neutral-700 p-4 text-center transition-all hover:border-blue-300 hover:bg-blue-100 mx-2"
          >
            {{ feature.label }}
          </button>
        </div>
      </div>
    </Transition>

    <!-- Slot untuk content halaman -->
    <slot />
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
