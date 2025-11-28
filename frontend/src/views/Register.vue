<template>
  <div class="min-h-screen flex items-center justify-center px-4 py-12">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white">
          Zarejestruj się
        </h2>
        <p class="mt-2 text-gray-600 dark:text-gray-400">
          Masz już konto? 
          <router-link to="/login" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">
            Zaloguj się
          </router-link>
        </p>
      </div>
      
      <div class="card">
        <form @submit.prevent="handleRegister" class="space-y-6">
          <!-- Komunikat błędu -->
          <div v-if="errorMessage" class="bg-red-50 dark:bg-red-900/20 border border-red-300 dark:border-red-800 text-red-800 dark:text-red-300 px-4 py-3 rounded-lg">
            {{ errorMessage }}
          </div>
          
          <!-- Komunikat sukcesu -->
          <div v-if="successMessage" class="bg-green-50 dark:bg-green-900/20 border border-green-300 dark:border-green-800 text-green-800 dark:text-green-300 px-4 py-3 rounded-lg">
            {{ successMessage }}
          </div>
          
          <!-- Username -->
          <div>
            <label for="username" class="block text-sm font-medium mb-2">
              Nazwa użytkownika
            </label>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              required
              minlength="3"
              class="input-field"
              placeholder="Minimum 3 znaki"
            />
          </div>
          
          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium mb-2">
              Email
            </label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              required
              class="input-field"
              placeholder="twoj@email.com"
            />
          </div>
          
          <!-- Hasło -->
          <div>
            <label for="password" class="block text-sm font-medium mb-2">
              Hasło
            </label>
            <input
              id="password"
              v-model="formData.password"
              type="password"
              required
              minlength="6"
              class="input-field"
              placeholder="Minimum 6 znaków"
            />
          </div>
          
          <!-- Potwierdzenie hasła -->
          <div>
            <label for="confirmPassword" class="block text-sm font-medium mb-2">
              Potwierdź hasło
            </label>
            <input
              id="confirmPassword"
              v-model="formData.confirmPassword"
              type="password"
              required
              class="input-field"
              placeholder="Powtórz hasło"
            />
          </div>
          
          <!-- Przycisk rejestracji -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full btn-primary py-3"
          >
            <span v-if="loading">Rejestracja...</span>
            <span v-else>Zarejestruj się</span>
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
  name: 'Register',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const formData = ref({
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })
    
    const loading = ref(false)
    const errorMessage = ref('')
    const successMessage = ref('')
    
    const handleRegister = async () => {
      loading.value = true
      errorMessage.value = ''
      successMessage.value = ''
      
      // Walidacja hasła
      if (formData.value.password !== formData.value.confirmPassword) {
        errorMessage.value = 'Hasła nie są identyczne'
        loading.value = false
        return
      }
      
      const result = await authStore.register({
        username: formData.value.username,
        email: formData.value.email,
        password: formData.value.password
      })
      
      loading.value = false
      
      if (result.success) {
        successMessage.value = 'Rejestracja zakończona pomyślnie! Przekierowanie do logowania...'
        setTimeout(() => {
          router.push('/login')
        }, 2000)
      } else {
        errorMessage.value = result.error
      }
    }
    
    return {
      formData,
      loading,
      errorMessage,
      successMessage,
      handleRegister
    }
  }
}
</script>
