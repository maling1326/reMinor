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

function closeAndClear() {
  // Clear any pending session data if the user clicks outside to cancel
  features.forEach((feature) => {
    sessionStorage.removeItem(`${feature.namespace}_pending`);
  });
  emit("close");
}

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
  <Transition name="modal-pop">
    <!-- Backdrop -->
    <div
      v-if="show"
      class="fixed inset-0 bg-black/60 backdrop-blur-md flex items-center justify-center z-50 p-4"
      @click.self="closeAndClear"
    >
      <!-- Modal Card -->
      <div
        class="bg-primary relative overflow-hidden flex flex-col rounded-[2rem] max-w-lg w-full p-6 md:p-8 border border-white/10 shadow-2xl shadow-black/80"
      >
        <!-- Decorative Ambient Glows -->
        <div
          class="absolute -top-20 -left-20 w-48 h-48 bg-secondary/15 rounded-full blur-[50px] pointer-events-none"
        ></div>
        <div
          class="absolute -bottom-20 -right-20 w-48 h-48 bg-tertiary/15 rounded-full blur-[50px] pointer-events-none"
        ></div>

        <!-- Header -->
        <div class="flex justify-between items-center mb-6 relative z-10">
          <p class="text-2xl font-bold text-secondary!">Pilih Fitur</p>
          <button
            @click="closeAndClear"
            class="w-10 h-10 rounded-full bg-white/5 border border-white/10 flex items-center justify-center hover:bg-red-500/20 hover:border-red-500/30 transition-all duration-300 group"
          >
            <svg
              class="w-5 h-5 text-white/50 group-hover:text-red-400 transition-colors"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        <!-- Features Grid -->
        <div class="grid grid-cols-2 gap-4 relative z-10">
          <button
            v-for="(feature, index) in features"
            :key="feature.path + index"
            @click="selectFeatures(feature.path, feature.namespace)"
            class="group flex flex-col items-center justify-center gap-3 p-5 rounded-2xl border border-white/5 bg-white/5 transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:bg-white/10"
            :class="
              index % 2 === 0
                ? 'hover:border-secondary/50 hover:shadow-secondary/10'
                : 'hover:border-tertiary/50 hover:shadow-tertiary/10'
            "
          >
            <!-- Icon Wrapper -->
            <div
              class="w-12 h-12 rounded-xl flex items-center justify-center bg-black/20 border border-white/5 group-hover:scale-110 transition-transform duration-300"
              :class="
                index % 2 === 0
                  ? 'text-secondary/80 group-hover:text-secondary group-hover:border-secondary/30'
                  : 'text-tertiary/80 group-hover:text-tertiary group-hover:border-tertiary/30'
              "
            >
              <!-- Dynamic Icons based on label -->
              <svg
                v-if="feature.label.toLowerCase() === 'compress'"
                class="w-6 h-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M4 14h6v6M20 10h-6V4M14 10l7-7M10 14l-7 7"
                />
              </svg>
              <svg
                v-else-if="feature.label.toLowerCase() === 'convert'"
                class="w-6 h-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"
                />
              </svg>
              <svg
                v-else-if="feature.label.toLowerCase() === 'resize'"
                class="w-6 h-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <rect
                  x="3"
                  y="3"
                  width="18"
                  height="18"
                  rx="2"
                  ry="2"
                  stroke-dasharray="4 4"
                />
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M21 15l-5-5L5 21"
                />
              </svg>
              <svg
                v-else-if="feature.label.toLowerCase() === 'adjust'"
                class="w-6 h-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M4 6h16M4 12h16M4 18h16"
                />
                <circle cx="10" cy="6" r="2" fill="currentColor" />
                <circle cx="16" cy="12" r="2" fill="currentColor" />
              </svg>
              <svg
                v-else
                class="w-6 h-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"
                />
              </svg>
            </div>

            <span
              class="text-base font-bold text-white! tracking-wide transition-colors"
              :class="
                index % 2 === 0
                  ? 'group-hover:text-secondary!'
                  : 'group-hover:text-tertiary!'
              "
            >
              {{ feature.label }}
            </span>
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
/* Smooth scale/fade entry matching native Apple dialogs */
.modal-pop-enter-active,
.modal-pop-leave-active {
  transition: opacity 0.4s ease;
}

.modal-pop-enter-from,
.modal-pop-leave-to {
  opacity: 0;
}

.modal-pop-enter-active > div {
  transition: all 0.5s cubic-bezier(0.22, 1, 0.36, 1);
}

.modal-pop-leave-active > div {
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.modal-pop-enter-from > div {
  opacity: 0;
  transform: scale(0.9) translateY(20px);
}

.modal-pop-leave-to > div {
  opacity: 0;
  transform: scale(0.95) translateY(10px);
}
</style>
