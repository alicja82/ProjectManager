<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
          Moje Projekty
        </h1>
        <p class="mt-1 text-gray-600 dark:text-gray-400">
          Zarządzaj swoimi projektami i zadaniami
        </p>
      </div>
      
      <button @click="showCreateModal = true" class="btn-primary">
        + Nowy projekt
      </button>
    </div>
    
    <!-- Loading -->
    <div v-if="loading" class="text-center py-12">
      <div class="text-gray-600 dark:text-gray-400">Ładowanie projektów...</div>
    </div>
    
    <!-- Brak projektów -->
    <div v-else-if="projects.length === 0" class="text-center py-12">
      <svg class="w-20 h-20 mx-auto mb-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/>
      </svg>
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
        Nie masz jeszcze żadnych projektów
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        Utwórz swój pierwszy projekt, aby rozpocząć
      </p>
      <button @click="showCreateModal = true" class="btn-primary">
        Utwórz projekt
      </button>
    </div>
    
    <!-- Lista projektów -->
    <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="project in projects" 
        :key="project.id"
        class="card hover:shadow-lg transition-shadow cursor-pointer"
        @click="goToProject(project.id)"
      >
        <div class="flex justify-between items-start mb-4">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
            {{ project.name }}
          </h3>
          <span 
            v-if="project.owner_id === user?.id"
            class="px-2 py-1 bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 text-xs rounded-full"
          >
            Owner
          </span>
        </div>
        
        <p class="text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
          {{ project.description || 'Brak opisu' }}
        </p>
        
        <div class="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
          <div class="flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
            </svg>
            <span>{{ project.owner?.username }}</span>
          </div>
          <div class="flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
            <span>{{ formatDate(project.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Modal tworzenia projektu -->
    <div 
      v-if="showCreateModal" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click.self="showCreateModal = false"
    >
      <div class="bg-white dark:bg-gray-800 rounded-lg max-w-md w-full p-6">
        <h2 class="text-2xl font-bold mb-4">Nowy projekt</h2>
        
        <form @submit.prevent="handleCreateProject" class="space-y-4">
          <div v-if="errorMessage" class="bg-red-50 dark:bg-red-900/20 border border-red-300 dark:border-red-800 text-red-800 dark:text-red-300 px-4 py-3 rounded-lg text-sm">
            {{ errorMessage }}
          </div>
          
          <div>
            <label for="projectName" class="block text-sm font-medium mb-2">
              Nazwa projektu *
            </label>
            <input
              id="projectName"
              v-model="newProject.name"
              type="text"
              required
              class="input-field"
              placeholder="Wprowadź nazwę projektu"
            />
          </div>
          
          <div>
            <label for="projectDescription" class="block text-sm font-medium mb-2">
              Opis (opcjonalnie)
            </label>
            <textarea
              id="projectDescription"
              v-model="newProject.description"
              rows="3"
              class="input-field resize-none"
              placeholder="Opisz swój projekt..."
            ></textarea>
          </div>
          
          <div class="flex justify-end space-x-3">
            <button 
              type="button" 
              @click="showCreateModal = false" 
              class="btn-secondary"
            >
              Anuluj
            </button>
            <button 
              type="submit" 
              :disabled="creatingProject"
              class="btn-primary"
            >
              {{ creatingProject ? 'Tworzenie...' : 'Utwórz' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useProjectsStore } from '../stores/projects'

export default {
  name: 'Dashboard',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const projectsStore = useProjectsStore()
    
    const showCreateModal = ref(false)
    const creatingProject = ref(false)
    const errorMessage = ref('')
    
    const newProject = ref({
      name: '',
      description: ''
    })
    
    const user = computed(() => authStore.user)
    const projects = computed(() => projectsStore.projects)
    const loading = computed(() => projectsStore.loading)
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('pl-PL')
    }
    
    const goToProject = (id) => {
      router.push(`/projects/${id}`)
    }
    
    const handleCreateProject = async () => {
      creatingProject.value = true
      errorMessage.value = ''
      
      const result = await projectsStore.createProject(newProject.value)
      
      creatingProject.value = false
      
      if (result.success) {
        showCreateModal.value = false
        newProject.value = { name: '', description: '' }
      } else {
        errorMessage.value = result.error
      }
    }
    
    onMounted(() => {
      projectsStore.fetchProjects()
    })
    
    return {
      user,
      projects,
      loading,
      showCreateModal,
      creatingProject,
      errorMessage,
      newProject,
      formatDate,
      goToProject,
      handleCreateProject
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
