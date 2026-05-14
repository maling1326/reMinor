<template>
  <div>
    <h1 class="text-4xl font-bold">Hello nigga</h1>

    <div
      class="max-w-md grid grid-cols-1 gap-2 border-2 border-gray-700 m-4 p-2"
    >
      <h1 class="p-2 text-2xl font-bold">You clicked {{ counter }} times!</h1>
      <button @click="counter++" class="p-2 bg-blue-500 text-white rounded">
        Click me
      </button>
      <button @click="counter = 0" class="p-2 border-2 border-black rounded">
        Reset Counter
      </button>
    </div>

    <p v-if="pending">loading...</p>
    <div
      v-else
      class="max-w-md grid grid-cols-1 gap-2 border-2 border-gray-700 m-4 p-2"
    >
      <h1>You have {{ data?.fruits.length }} fruits!</h1>
      <ul class="list-disc list-inside p-4">
        <li v-for="fruit in data?.fruits" :key="fruit.id">
          {{ fruit.name }}
        </li>
      </ul>
    </div>
  </div>
  <h1 class="text-xl font-bold">{{ tempData?.message }}</h1>
  <input type="file" accept="image/*" @change="handleFile" />
  <img v-if="preview" :src="preview" alt="selected image" class="max-w-125" />

  <h1 class="text-md font-black">Compressed Image</h1>
  <img v-if="result" :src="result" alt="compressed image" class="max-w-125" />
</template>

<script lang="ts" setup>
useHead({
  title: "DownScaler",
});

const counter = useState<number>("count", () => 0);

const { data, pending, error } = useFetch("/api/hello", { server: false });

const response = await fetch("http://localhost:8000/");
const tempData = await response.json();

const preview = ref<string | null>(null);
const result = ref<string | null>(null);

async function handleFile(event: Event) {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (!file) return;

  preview.value = URL.createObjectURL(file);

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://localhost:8000/compress", {
    method: "POST",
    body: formData,
  });

  const blob = await response.blob();
  result.value = URL.createObjectURL(blob);
}
</script>
