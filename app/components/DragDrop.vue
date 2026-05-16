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

const isFeaturePage = computed(() => featureRoutes.includes(route.path));

function onDragEnter(e: DragEvent) {
  e.preventDefault();
  isDragging.value = true;
}

function onDragLeave(e: DragEvent) {
  if (e.relatedTarget === null) isDragging.value = false;
}

function onDragOver(e: DragEvent) {
  e.preventDefault();
}

async function onDrop(e: DragEvent) {
  e.preventDefault();
  isDragging.value = false;

  const file = e.dataTransfer?.files[0];
  if (!file || !file.type.startsWith("image/")) return;

  pendingFile.value = file;

  if (isFeaturePage.value) {
    await loadToCurrentPage();
  } else {
    showModal.value = true;
  }
}

async function loadToCurrentPage() {
  if (!pendingFile.value) return;

  const feature = features.find((f) => f.path === route.path);
  if (!feature) return;

  const reader = new FileReader();
  const base64 = await new Promise<string>((resolve, reject) => {
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = reject;
    reader.readAsDataURL(pendingFile.value!);
  });

  sessionStorage.setItem(`${feature.namespace}_pending`, base64);
  window.dispatchEvent(
    new CustomEvent("dragdrop:newfile", {
      detail: { namespace: feature.namespace },
    }),
  );
}

onMounted(() => {
  window.addEventListener("filepicker:newfile", async (e: Event) => {
    const { file } = (e as CustomEvent).detail;
    if (!file) return;
    pendingFile.value = file;
    if (isFeaturePage.value) {
      await loadToCurrentPage();
    } else {
      showModal.value = true;
    }
  });
});

onUnmounted(() => {
  window.removeEventListener("filepicker:newfile", () => {});
});
</script>

<template>
  <div
    class="min-h-screen"
    @dragenter="onDragEnter"
    @dragleave="onDragLeave"
    @dragover="onDragOver"
    @drop="onDrop"
  >
    <Transition name="fade">
      <div
        v-if="isDragging"
        class="fixed inset-0 bg-blue-500/30 border-4 border-dashed border-blue-500 z-50 flex items-center justify-center pointer-events-none"
      >
        <p class="text-blue-700 text-4xl font-bold">Drop gambar di sini!</p>
      </div>
    </Transition>

    <!-- ✅ pakai FeatureModal -->
    <FeatureModal
      :show="showModal"
      :pendingFile="pendingFile"
      @close="showModal = false"
    />

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
