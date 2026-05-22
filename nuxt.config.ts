import tailwindcss from "@tailwindcss/vite";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      // Default to localhost if the environment variable isn't set
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
    },
  },

  compatibilityDate: "2025-07-15",
  devtools: { enabled: false },
  css: ["~/assets/css/main.css"],

  vite: {
    plugins: [tailwindcss()],

    server: {
      allowedHosts: ["reentry-strangely-evacuate.ngrok-free.dev", "*"],
    },
  },

  modules: ["@nuxt/fonts"],

  app: {
    head: {
      title: "reMinor",
      titleTemplate: "reMinor - %s",
    },
  },
});
