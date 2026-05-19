export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.directive("appear", {
    mounted: (el: HTMLElement, binding: any) => {
      const delay = binding.value || 0;

      // Initial state
      el.style.opacity = "0";
      el.style.transform = "translateY(-40px) scale(0.98)";
      el.style.filter = "blur(10px)";
      el.style.transition = `all 1.2s cubic-bezier(0.22, 1, 0.36, 1) ${delay}ms`;

      // Observe when entering viewport
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              // Settle into place
              el.style.opacity = "1";
              el.style.transform = "translateY(0) scale(1)";
              el.style.filter = "blur(0)";
              observer.unobserve(el);
            }
          });
        },
        { threshold: 0.15 },
      );

      observer.observe(el);
    },
  });
});
