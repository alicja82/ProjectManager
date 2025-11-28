<template>
  <nav class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <router-link to="/" class="flex items-center">
            <span class="text-2xl font-bold text-primary-600 dark:text-primary-400">
              ProjectManager
            </span>
          </router-link>
        </div>
        
        <div class="flex items-center space-x-4">
          <!-- Przełącznik motywu -->
          <button 
            @click="toggleTheme" 
            class="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            :title="isDark ? 'Przełącz na tryb jasny' : 'Przełącz na tryb ciemny'"
          >
            <svg v-if="isDark" class="w-6 h-6 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"/>
            </svg>
            <svg v-else class="w-6 h-6 text-gray-700" fill="currentColor" viewBox="0 0 20 20">
              <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"/>
            </svg>
          </button>
          
          <!-- Menu użytkownika -->
          <div v-if="isAuthenticated" class="flex items-center space-x-3">
            <span class="text-sm text-gray-700 dark:text-gray-300">
              Witaj, <strong>{{ user?.username }}</strong>
            </span>
            <button 
              @click="handleLogout" 
              class="btn-secondary text-sm"
            >
              Wyloguj
            </button>
          </div>
          
          <!-- Przyciski logowania/rejestracji -->
          <div v-else class="flex items-center space-x-2">
            <router-link to="/login" class="btn-secondary text-sm">
              Zaloguj
            </router-link>
            <router-link to="/register" class="btn-primary text-sm">
              Zarejestruj się
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useThemeStore } from '../stores/theme'

export default {
  name: 'Navbar',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const themeStore = useThemeStore()
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const user = computed(() => authStore.user)
    const isDark = computed(() => themeStore.isDark)
    
    const toggleTheme = () => {
      themeStore.toggleTheme()
    }
    
    const handleLogout = () => {
      authStore.logout()
      router.push('/')
    }
    
    return {
      isAuthenticated,
      user,
      isDark,
      toggleTheme,
      handleLogout
    }
  }
}
</script>
