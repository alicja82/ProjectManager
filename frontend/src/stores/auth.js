import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '../api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  function loadFromStorage() {
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')
    
    if (savedToken && savedUser) {
      token.value = savedToken
      user.value = JSON.parse(savedUser)
    }
  }

  async function register(credentials) {
    loading.value = true
    error.value = null
    
    try {
      const response = await authAPI.register(credentials)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.error || 'Błąd rejestracji'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function login(credentials) {
    loading.value = true
    error.value = null
    
    try {
      const response = await authAPI.login(credentials)
      const { access_token, user: userData } = response.data
      
      token.value = access_token
      user.value = userData
      
      // Persystencja w localStorage - token przetrwa odświeżenie strony
      localStorage.setItem('token', access_token)
      localStorage.setItem('user', JSON.stringify(userData))
      
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Błąd logowania'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  async function fetchCurrentUser() {
    try {
      const response = await authAPI.getCurrentUser()
      user.value = response.data.user
      localStorage.setItem('user', JSON.stringify(response.data.user))
    } catch (err) {
      console.error('Błąd pobierania użytkownika:', err)
      logout()
    }
  }

  loadFromStorage()

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    register,
    login,
    logout,
    fetchCurrentUser
  }
})
