<script setup>
// Optional: Explicitly tell Nuxt this is a 404 response for SEO
setResponseStatus(404);
</script>

<template>
  <div class="w-full h-dvh flex justify-center items-center">
    <div class="text-center py-20">
      <div class="flex justify-center items-center">
        <img src="assets/img/Kaela.png" class="w-24" />
      </div>
      <h1 class="text-4xl font-bold mb-4">Page Not Found</h1>
      <p class="mb-8">The route you are looking for doesn't exist yet.</p>

      <NuxtLink to="/" class="text-blue-500 underline"> Return Home </NuxtLink>
    </div>
  </div>
</template>
