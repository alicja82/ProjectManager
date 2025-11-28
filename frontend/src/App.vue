<template>
  <div id="app">
    <Navbar />
    <main class="min-h-screen">
      <router-view />
    </main>
  </div>
</template>

<script>
import { onMounted, watch } from 'vue'
import { useThemeStore } from './stores/theme'
import Navbar from './components/Navbar.vue'

export default {
  name: 'App',
  components: {
    Navbar
  },
  setup() {
    const themeStore = useThemeStore()

    const updateTheme = () => {
      if (themeStore.isDark) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }

    onMounted(() => {
      updateTheme()
    })

    watch(() => themeStore.isDark, () => {
      updateTheme()
    })

    return {}
  }
}
</script>
