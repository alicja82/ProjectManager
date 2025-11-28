<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="max-w-3xl mx-auto text-center">
      <h1 class="text-5xl md:text-6xl font-bold mb-6 text-gray-900 dark:text-white">
        <span class="text-primary-600 dark:text-primary-400">ProjectManager</span>
      </h1>
      
      <p class="text-xl text-gray-600 dark:text-gray-300 mb-12">
        Zarządzaj projektami i zadaniami w jednym miejscu.
        Współpracuj z zespołem i osiągaj cele efektywnie.
      </p>
      
      <div class="flex flex-col sm:flex-row gap-4 justify-center mb-16">
        <router-link to="/register" class="btn-primary text-lg px-8 py-3">
          Rozpocznij za darmo
        </router-link>
        <router-link to="/login" class="btn-secondary text-lg px-8 py-3">
          Zaloguj się
        </router-link>
      </div>
      
      <div class="grid md:grid-cols-3 gap-6">
        <div class="p-6">
          <svg class="w-12 h-12 mx-auto mb-3 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"/>
          </svg>
          <h3 class="text-lg font-semibold mb-2">Projekty</h3>
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            Twórz i zarządzaj projektami zespołowymi
          </p>
        </div>
        
        <div class="p-6">
          <svg class="w-12 h-12 mx-auto mb-3 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/>
          </svg>
          <h3 class="text-lg font-semibold mb-2">Zadania</h3>
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            Organizuj pracę z prostymi statusami
          </p>
        </div>
        
        <div class="p-6">
          <svg class="w-12 h-12 mx-auto mb-3 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
          </svg>
          <h3 class="text-lg font-semibold mb-2">Zespół</h3>
          <p class="text-gray-600 dark:text-gray-400 text-sm">
            Współpracuj i przypisuj zadania
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Home',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    onMounted(() => {
      // Przekieruj zalogowanych użytkowników do dashboard
      if (authStore.isAuthenticated) {
        router.push('/dashboard')
      }
    })
  }
}
</script>
