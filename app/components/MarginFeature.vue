<template>
  <!-- 
    Make the outermost wrapper the master scroll container.
    Added snap-y so children can still use CSS scroll snapping. 
  -->
  <div
    class="w-full h-dvh overflow-y-auto overflow-x-hidden snap-y snap-mandatory scroll-smooth"
  >
    <div class="w-full min-h-full flex justify-center">
      <div
        class="max-w-7xl w-full py-24 sm:py-28 px-4 sm:px-8 flex flex-col .no-scrollbar"
      >
        <slot />
      </div>
    </div>
  </div>
</template>
