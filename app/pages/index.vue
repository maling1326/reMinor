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
</template>

<script lang="ts" setup>
useHead({
  title: "DownScaler",
});

const counter = useState<number>("count", () => 0);

const { data, pending, error } = useFetch("/api/hello", { server: false });
</script>
