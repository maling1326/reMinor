<script lang="ts" setup>
const { fileInput, openFilePicker, onFileChange, showModal, pendingFile } =
  useFilePicker();
</script>

<template>
  <FeatureModal
    :show="showModal"
    :pendingFile="pendingFile"
    @close="showModal = false"
  />
  <MarginDefault>
    <!-- 
      SECTION 1: Kompres Lossless
    -->
    <section
      class="w-full h-dvh snap-center snap-always flex justify-center items-center overflow-hidden px-8 lg:px-25 pt-20"
    >
      <div
        class="grid grid-cols-1 md:grid-cols-2 gap-10 lg:gap-20 items-stretch max-w-7xl w-full"
      >
        <!-- Text Content -->
        <div class="w-full flex flex-col justify-center gap-8" v-appear>
          <h1 class="font-bold text-5xl lg:text-6xl">
            Kompres
            <span class="font-black text-7xl lg:text-8xl text-brand"
              >Lossless</span
            >
          </h1>

          <p class="text-[22px] text-base/65!">
            Kompresi ukuran citra tanpa mengubah resolusi atau kejernihan pixel
            menggunakan algoritma yang sudah teruji klinis.
          </p>

          <div>
            <button
              @click="openFilePicker"
              class="bg-secondary py-3 rounded-base px-6 hover:bg-secondary-dark border hover:border-secondary-dark transition-all text-[20px] font-medium text-primary! shadow-lg shadow-secondary/20"
            >
              Upload Gambar
            </button>

            <!-- hidden input -->
            <input
              ref="fileInput"
              type="file"
              accept="image/*"
              class="hidden"
              @change="onFileChange"
            />
            <p class="text-base/40! mt-2 font-medium">*.JPG, *PNG, *JPEG</p>
          </div>
        </div>

        <!-- Image Content -->
        <div class="w-full flex justify-end items-center" v-appear="200">
          <div
            class="p-4 rounded-base bg-secondary w-full max-w-106.25 shadow-2xl shadow-black/40 hover:scale-[1.02] transition-transform duration-500"
          >
            <div
              class="flex w-full max-h-106.25 overflow-hidden rounded-[10px]"
            >
              <!-- Original Image -->
              <div
                class="w-1/2 overflow-hidden relative border-r border-transparent"
              >
                <img
                  src="~/assets/img/compress_original.jpg"
                  alt="Before"
                  class="w-[200%] max-w-none object-cover block"
                />
                <p
                  class="absolute bottom-5 left-5 bg-primary/40 backdrop-blur-sm rounded-2xl px-3 py-1 shadow-lg text-base/80! text-sm font-medium"
                >
                  > 903 KB
                </p>
              </div>

              <!-- Result Image -->
              <div
                class="w-1/2 overflow-hidden relative border-r border-transparent"
              >
                <img
                  src="~/assets/img/compress_result.jpg"
                  alt="After"
                  class="w-[200%] max-w-none object-cover block -translate-x-1/2"
                />
                <p
                  class="absolute bottom-5 right-5 bg-primary/60 backdrop-blur-md rounded-2xl px-3 py-1 shadow-lg text-secondary! text-sm font-bold border border-secondary/30"
                >
                  ~ 100 KB
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 
      SECTION 2: Showcase App Window
    -->
    <section
      class="w-full h-dvh snap-center snap-always flex justify-center items-center overflow-hidden px-4 md:px-8 lg:px-25 pt-24 pb-8"
    >
      <div
        class="w-full h-[90%] max-h-200 rounded-4xl bg-[#222222] border border-white/10 shadow-2xl shadow-black/60 max-w-7xl relative overflow-hidden flex flex-col group"
        v-appear
      >
        <!-- App Window Header -->
        <div
          class="w-full h-12 min-h-12 flex items-center px-6 gap-2 bg-white/5 border-b border-white/5"
        >
          <div class="w-3.5 h-3.5 rounded-full bg-red-400/80"></div>
          <div class="w-3.5 h-3.5 rounded-full bg-yellow-400/80"></div>
          <div class="w-3.5 h-3.5 rounded-full bg-green-400/80"></div>
          <p
            class="ml-4 text-xs font-medium text-white/30! tracking-widest uppercase"
          >
            reMinor Workspace
          </p>
        </div>

        <!-- App Window Content -->
        <div
          class="w-full flex-1 flex flex-col items-center pt-10 md:pt-16 px-6 lg:px-20 relative"
        >
          <div class="text-center z-20 max-w-2xl mb-8" v-appear="200">
            <h2 class="font-bold text-4xl lg:text-5xl text-white! mb-4">
              All-in-one <span class="text-brand">Workspace</span>
            </h2>
            <p class="text-[18px] text-white/60!">
              Tampilan antarmuka yang bersih dan intuitif, dirancang untuk
              mempermudah alur kerja Anda dengan alat AI canggih di genggaman.
            </p>
          </div>

          <!-- The Image popping from the bottom -->
          <div
            class="w-full flex-1 relative flex justify-center items-end mt-4"
            v-appear="400"
          >
            <!-- Glow effect behind image -->
            <div
              class="absolute inset-x-0 bottom-0 h-1/2 bg-brand/10 blur-[100px] rounded-full translate-y-1/2"
            ></div>

            <img
              src="~/assets/img/compress_thumbnail.png"
              alt="Thumbnail Compress"
              class="w-full md:w-10/12 lg:w-4/5 object-cover rounded-t-2xl shadow-2xl shadow-black border border-b-0 border-white/10 z-10 transform translate-y-4 group-hover:translate-y-1 transition-transform duration-700 ease-out"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- 
      SECTION 3: Feature Grid
    -->
    <section
      class="w-full h-dvh snap-center snap-always flex justify-center items-center overflow-hidden px-4 md:px-8 lg:px-25 pt-20"
    >
      <div
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-y-12 gap-x-8 max-w-7xl w-full"
      >
        <!-- Feature 1: Invert -->
        <div
          class="flex flex-col items-center text-center gap-4 group"
          v-appear="0"
        >
          <div
            class="w-20 h-20 rounded-2xl bg-tertiary border-2 border-tertiary flex items-center justify-center mb-2 shadow-lg shadow-tertiary/20 group-hover:scale-110 transition-transform duration-300"
          >
            <svg
              class="w-10 h-10 text-primary"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M4.93 4.93l14.14 14.14"
              />
            </svg>
          </div>
          <h3 class="font-bold text-2xl">Invert</h3>
          <p class="text-white/50! text-[16px] leading-relaxed max-w-xs">
            Balikkan skema warna citra untuk menciptakan efek visual klise atau
            memperjelas detail pada objek tertentu
          </p>
        </div>

        <!-- Feature 2: Compress -->
        <div
          class="flex flex-col items-center text-center gap-4 group"
          v-appear="100"
        >
          <div
            class="w-20 h-20 rounded-2xl bg-secondary border-2 border-secondary flex items-center justify-center mb-2 shadow-lg shadow-secondary/20 group-hover:scale-110 transition-transform duration-300"
          >
            <svg
              class="w-10 h-10 text-primary"
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
          </div>
          <h3 class="font-bold text-2xl">Compress</h3>
          <p class="text-white/50! text-[16px] leading-relaxed max-w-xs">
            Optimalkan ukuran file gambar secara efisien tanpa mengurangi
            kualitas visual asli
          </p>
        </div>

        <!-- Feature 3: Resize -->
        <div
          class="flex flex-col items-center text-center gap-4 group"
          v-appear="200"
        >
          <div
            class="w-20 h-20 rounded-2xl bg-tertiary border-2 border-tertiary flex items-center justify-center mb-2 shadow-lg shadow-tertiary/20 group-hover:scale-110 transition-transform duration-300"
          >
            <svg
              class="w-10 h-10 text-primary"
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
              <circle cx="8.5" cy="8.5" r="1.5" fill="currentColor" />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M21 15l-5-5L5 21"
              />
            </svg>
          </div>
          <h3 class="font-bold text-2xl">Resize</h3>
          <p class="text-white/50! text-[16px] leading-relaxed max-w-xs">
            Sesuaikan dimensi panjang dan lebar foto secara presisi untuk
            berbagai kebutuhan
          </p>
        </div>

        <!-- Feature 4: Crop -->
        <div
          class="flex flex-col items-center text-center gap-4 group"
          v-appear="300"
        >
          <div
            class="w-20 h-20 rounded-2xl bg-secondary border-2 border-secondary flex items-center justify-center mb-2 shadow-lg shadow-secondary/20 group-hover:scale-110 transition-transform duration-300"
          >
            <svg
              class="w-10 h-10 text-primary"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M6 2v16h16M22 6H6"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M18 22V6H2"
              />
            </svg>
          </div>
          <h3 class="font-bold text-2xl">Crop</h3>
          <p class="text-white/50! text-[16px] leading-relaxed max-w-xs">
            Sesuaikan komposisi foto dengan memotong area yang tidak diinginkan
          </p>
        </div>

        <!-- Feature 5: Adjust -->
        <div
          class="flex flex-col items-center text-center gap-4 group"
          v-appear="400"
        >
          <div
            class="w-20 h-20 rounded-2xl bg-tertiary border-2 border-tertiary flex items-center justify-center mb-2 shadow-lg shadow-tertiary/20 group-hover:scale-110 transition-transform duration-300"
          >
            <svg
              class="w-10 h-10 text-primary"
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
              <circle cx="8" cy="18" r="2" fill="currentColor" />
            </svg>
          </div>
          <h3 class="font-bold text-2xl">Adjust</h3>
          <p class="text-white/50! text-[16px] leading-relaxed max-w-xs">
            Sempurnakan kualitas visual dengan mengatur tingkat kecerahan,
            kontras, dan saturasi warna secara instan
          </p>
        </div>

        <!-- Feature 6: Convert -->
        <div
          class="flex flex-col items-center text-center gap-4 group"
          v-appear="500"
        >
          <div
            class="w-20 h-20 rounded-2xl bg-secondary border-2 border-secondary flex items-center justify-center mb-2 shadow-lg shadow-secondary/20 group-hover:scale-110 transition-transform duration-300"
          >
            <svg
              class="w-10 h-10 text-primary"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
          </div>
          <h3 class="font-bold text-2xl">Convert</h3>
          <p class="text-white/50! text-[16px] leading-relaxed max-w-xs">
            Ubah format file gambar Anda ke berbagai tipe ekstensi populer
            dengan tetap menjaga integritas data
          </p>
        </div>
      </div>
    </section>

    <!-- 
      SECTION 4: Quote Box
    -->
    <section
      class="w-full h-dvh snap-center snap-always flex justify-center items-center overflow-hidden px-4 md:px-8 lg:px-25 pt-20"
    >
      <div
        class="w-full max-w-7xl h-[60dvh] max-h-150 bg-secondary rounded-4xl flex flex-col justify-center items-center p-8 md:p-16 text-center shadow-2xl shadow-secondary/20 relative overflow-hidden group"
        v-appear
      >
        <!-- Floating quote icons -->
        <svg
          class="w-24 h-24 text-primary! mb-8"
          fill="currentColor"
          viewBox="0 0 24 24"
          v-appear="200"
        >
          <path
            d="M14.017 21v-7.391c0-5.704 3.731-9.57 8.983-10.609l.995 2.151c-2.432.917-3.995 3.638-3.995 5.849h4v10h-9.983zm-14.017 0v-7.391c0-5.704 3.748-9.57 9-10.609l.996 2.151c-2.433.917-3.996 3.638-3.996 5.849h3.983v10h-9.983z"
          />
        </svg>

        <h2
          class="text-3xl md:text-4xl text-primary! font-medium leading-relaxed max-w-4xl"
          v-appear="400"
        >
          Melihat hasilnya adalah bukti nyata. Ini bukan sekadar kompresi, ini
          adalah menjaga kenangan dalam kualitas terbaiknya.
        </h2>

        <p
          class="mt-12 text-primary/60! font-medium text-xl tracking-wider"
          v-appear="600"
        >
          Sun Tzu
        </p>
      </div>
    </section>

    <!-- 
      SECTION 5: Testimonials
    -->
    <section
      class="w-full h-dvh snap-center snap-always flex justify-center items-center overflow-hidden px-4 md:px-8 lg:px-25 pt-20"
    >
      <div
        class="grid grid-cols-1 md:grid-cols-2 gap-8 lg:gap-12 max-w-7xl w-full"
      >
        <!-- Testimonial 1 -->
        <div
          class="bg-tertiary rounded-4xl p-8 md:p-12 flex flex-col justify-between min-h-100 shadow-2xl shadow-tertiary/10 hover:-translate-y-2 transition-transform duration-500"
          v-appear="0"
        >
          <p
            class="text-2xl md:text-[28px] font-bold text-primary! leading-snug"
          >
            Dulu foto saya gelap dan susah dilihat, tapi setelah pakai fitur
            adjust di web ini, semuanya jadi terang benderang. Sekarang saya
            jadi pusat perhatian!
          </p>
          <div class="flex items-center gap-5 mt-8">
            <img
              src="https://ui-avatars.com/api/?name=Pi+Guy&background=2B2B2B&color=f8d57e&size=150"
              alt="Pi Guy"
              class="w-16 h-16 rounded-full shadow-md object-cover border-2 border-primary/20"
            />
            <div>
              <p class="font-medium text-primary! text-xl mb-1">Pi Guy</p>
              <div class="flex gap-1 text-secondary">
                <!-- 3 Yellow, 2 Black stars -->
                <svg
                  v-for="i in 3"
                  :key="`yellow-${i}`"
                  class="w-5 h-5 fill-current"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279-7.416-3.967-7.417 3.967 1.481-8.279-6.064-5.828 8.332-1.151z"
                  />
                </svg>
                <svg
                  v-for="i in 2"
                  :key="`black-${i}`"
                  class="w-5 h-5 fill-current text-primary"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279-7.416-3.967-7.417 3.967 1.481-8.279-6.064-5.828 8.332-1.151z"
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>

        <!-- Testimonial 2 -->
        <div
          class="bg-tertiary rounded-4xl p-8 md:p-12 flex flex-col justify-between min-h-100 shadow-2xl shadow-tertiary/10 hover:-translate-y-2 transition-transform duration-500"
          v-appear="200"
        >
          <p
            class="text-2xl md:text-[28px] font-bold text-primary! leading-snug"
          >
            Dulu foto saya gelap dan susah dilihat, tapi setelah pakai fitur
            adjust di web ini, semuanya jadi terang benderang. Sekarang saya
            jadi pusat perhatian!
          </p>
          <div class="flex items-center gap-5 mt-8">
            <img
              src="https://ui-avatars.com/api/?name=Joko+Wi+Dodo&background=2B2B2B&color=f8d57e&size=150"
              alt="Joko Wi Dodo"
              class="w-16 h-16 rounded-full shadow-md object-cover border-2 border-primary/20"
            />
            <div>
              <p class="font-medium text-primary! text-xl mb-1">Joko Wi Dodo</p>
              <div class="flex gap-1 text-secondary">
                <!-- 5 Yellow stars -->
                <svg
                  v-for="i in 5"
                  :key="`yellow-2-${i}`"
                  class="w-5 h-5 fill-current"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279-7.416-3.967-7.417 3.967 1.481-8.279-6.064-5.828 8.332-1.151z"
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 
      SECTION 6: CTA
    -->
    <section
      class="w-full h-dvh snap-center snap-always flex justify-center items-center overflow-hidden px-4 md:px-8 lg:px-25 pt-20 relative"
    >
      <!-- Radial glow effect -->
      <div
        class="absolute inset-0 flex justify-center items-center pointer-events-none overflow-hidden"
      >
        <div
          class="w-[60vw] h-[60vw] max-w-200 max-h-200 bg-secondary/15 rounded-full blur-[100px] md:blur-[140px]"
        ></div>
      </div>

      <div
        class="max-w-3xl w-full flex flex-col items-center text-center z-10 gap-8"
      >
        <h2 class="font-bold text-6xl md:text-8xl text-white!" v-appear="0">
          Try <span class="text-secondary">reMinor</span> Now!
        </h2>

        <p
          class="text-xl md:text-2xl text-white/50 leading-relaxed max-w-2xl font-medium"
          v-appear="200"
        >
          Sempurnakan setiap piksel foto Anda dengan teknologi yang mengutamakan
          integritas visual dan efisiensi penyimpanan
        </p>

        <button
          @click="openFilePicker"
          class="mt-4 bg-secondary text-primary! font-bold px-12 py-4 rounded-xl text-xl hover:bg-secondary-dark transition-all duration-300 shadow-xl shadow-secondary/20 hover:scale-105"
          v-appear="400"
        >
          Try reMinor
        </button>
      </div>
    </section>
  </MarginDefault>
</template>
