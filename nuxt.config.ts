export default defineNuxtConfig({
  compatibilityDate: '2025-03-31',
  devtools: { enabled: false },

  modules: [
    '@nuxtjs/supabase',
    '@nuxtjs/tailwindcss',
  ],

  supabase: {
    redirectOptions: {
      login: '/login',
      callback: '/confirm',
      exclude: ['/', '/login'],
    },
  },

  app: {
    head: {
      title: 'OptiSleep - Sleep Smarter',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Track sleep, build streaks, and improve recovery with beautiful nightly analytics.' },
      ],
      link: [
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&display=swap' },
      ],
    },
  },
})
