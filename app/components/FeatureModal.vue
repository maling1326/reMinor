<script lang="ts" setup>
const features = [
  { label: "Compress", path: "/compress", namespace: "compress" },
  { label: "Convert", path: "/compress", namespace: "compress" },
  { label: "Resize", path: "/compress", namespace: "compress" },
  { label: "Adjust", path: "/compress", namespace: "compress" },
  { label: "minor", path: "/compress", namespace: "compress" },
  { label: "major", path: "/compress", namespace: "compress" },
];

const props = defineProps<{
  show: boolean;
  pendingFile: File | null;
}>();

const emit = defineEmits<{
  close: [];
}>();

async function selectFeatures(path: string, namespace: string) {
  if (!props.pendingFile) return;

  const reader = new FileReader();
  const base64 = await new Promise<string>((resolve, reject) => {
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = reject;
    reader.readAsDataURL(props.pendingFile!);
  });

  sessionStorage.setItem(`${namespace}_pending`, base64);
  emit("close");
  await navigateTo(path);
}
</script>

<template>
  <Transition name="fade">
    <div
      v-if="show"
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
