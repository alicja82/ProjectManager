<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-12">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white">
          Zaloguj się
        </h2>
        <p class="mt-2 text-gray-600 dark:text-gray-400">
          Nie masz konta? 
          <router-link to="/register" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">
            Zarejestruj się
          </router-link>
        </p>
      </div>
      
      <div class="card">
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div v-if="errorMessage" class="bg-red-50 dark:bg-red-900/20 border border-red-300 dark:border-red-800 text-red-800 dark:text-red-300 px-4 py-3 rounded-lg">
            {{ errorMessage }}
          </div>
          
          <div>
            <label for="username" class="block text-sm font-medium mb-2">
              Nazwa użytkownika
            </label>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              required
              class="input-field"
              placeholder="Wprowadź nazwę użytkownika"
            />
          </div>
          
          <div>
            <label for="password" class="block text-sm font-medium mb-2">
              Hasło
            </label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              required
              class="input-field"
              placeholder="Wprowadź hasło"
            />
          </div>
          
          <button
            type="submit"
            :disabled="loading"
            class="w-full btn-primary py-3"
          >
            <span v-if="loading">Logowanie...</span>
            <span v-else>Zaloguj się</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const formData = ref({
      username: '',
      password: ''
    })
    
    const loading = ref(false)
    const errorMessage = ref('')
    
    const handleLogin = async () => {
      loading.value = true
      errorMessage.value = ''
      
      const result = await authStore.login(formData.value)
      
      loading.value = false
      
      if (result.success) {
        router.push('/dashboard')
      } else {
        errorMessage.value = result.error
      }
    }
    
    return {
      formData,
      loading,
      errorMessage,
      handleLogin
    }
  }
}
</script>
