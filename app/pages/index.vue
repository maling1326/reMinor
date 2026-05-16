<template>
  <div>
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

    <h1 class="text-4xl font-bold">Hello nigga</h1>

    <label class="block mb-2.5 text-sm font-medium" for="file_input">
      Upload file
    </label>
    <input
      id="file_input"
      type="file"
      accept="image/*"
      @change="onFileChange"
      class="cursor-pointer border text-sm rounded-lg block w-min shadow-xs"
    />
  </div>
</template>

<script lang="ts" setup>
const showModal = ref(false);
let pendingFile = ref<File | null>(null); // ← simpan file sementara

const features = [
  { label: "Compress", path: "/compress", namespace: "compress" },
  { label: "Convert", path: "/compress", namespace: "compress" },
  { label: "Resize", path: "/compress", namespace: "compress" },
  { label: "Adjust", path: "/compress", namespace: "compress" },
  { label: "minor", path: "/compress", namespace: "compress" },
  { label: "major", path: "/compress", namespace: "compress" },
];

function onFileChange(event: Event) {
  const input = event.target as HTMLInputElement; // ← ambil element-nya
  const file = input.files?.[0];
  if (!file) return;

  pendingFile.value = file; // ← simpan file dulu
  showModal.value = true;
}

// index.vue
async function selectFeatures(path: string, namespace: string) {
  if (!pendingFile.value) return;

  // tunggu sampai base64 selesai ✅
  const reader = new FileReader();
  const base64 = await new Promise<string>((resolve, reject) => {
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = reject;
    reader.readAsDataURL(pendingFile.value!);
  });

  // baru simpan ke sessionStorage
  sessionStorage.setItem(`${namespace}_pending`, base64);

  // baru redirect
  await navigateTo(path);
}
</script>
