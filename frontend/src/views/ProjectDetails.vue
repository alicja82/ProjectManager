<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div v-if="loading" class="text-center py-12">
      <div class="text-gray-600 dark:text-gray-400">Ładowanie projektu...</div>
    </div>
    
    <div v-else-if="currentProject">
      <div class="mb-8">
        <div class="flex items-start justify-between mb-4">
          <div>
            <button @click="$router.push('/dashboard')" class="text-primary-600 hover:text-primary-700 mb-2 flex items-center">
              ← Powrót do Dashboard
            </button>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
              {{ currentProject.name }}
            </h1>
            <p class="text-gray-600 dark:text-gray-400 mt-2">
              {{ currentProject.description || 'Brak opisu' }}
            </p>
          </div>
          
          <div v-if="isOwner" class="flex space-x-2">
            <button @click="showEditModal = true" class="btn-secondary">
              Edytuj
            </button>
            <button @click="confirmDelete" class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg">
              Usuń
            </button>
          </div>
        </div>
        
        <div class="text-sm text-gray-500 dark:text-gray-400">
          Właściciel: <strong>{{ currentProject.owner?.username }}</strong> | 
          Utworzono: {{ formatDate(currentProject.created_at) }}
        </div>
      </div>
      
      <div class="grid lg:grid-cols-3 gap-6">
        <div class="lg:col-span-1">
          <div class="card">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-xl font-semibold">Członkowie ({{ members.length }})</h2>
              <button 
                v-if="isOwner"
                @click="showInviteModal = true" 
                class="text-primary-600 hover:text-primary-700"
              >
                + Dodaj
              </button>
            </div>
            
            <div class="space-y-3">
              <div 
                v-for="member in members" 
                :key="member.id"
                class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
              >
                <div>
                  <div class="font-medium">{{ member.user?.username }}</div>
                  <div class="text-xs text-gray-500 dark:text-gray-400">{{ member.role }}</div>
                </div>
                <button 
                  v-if="isOwner && member.user?.id !== currentProject.owner_id"
                  @click="handleRemoveMember(member.user?.id)"
                  class="text-red-600 hover:text-red-700 text-sm"
                >
                  Usuń
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="lg:col-span-2">
          <div class="card">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-xl font-semibold">Zadania</h2>
              <button @click="showTaskModal = true" class="btn-primary">
                + Nowe zadanie
              </button>
            </div>
            
            <div class="mb-4 flex space-x-2">
              <button 
                @click="filterStatus = null" 
                :class="filterStatus === null ? 'btn-primary' : 'btn-secondary'"
                class="text-sm"
              >
                Wszystkie
              </button>
              <button 
                @click="filterStatus = 'To do'" 
                :class="filterStatus === 'To do' ? 'btn-primary' : 'btn-secondary'"
                class="text-sm"
              >
                To do
              </button>
              <button 
                @click="filterStatus = 'In progress'" 
                :class="filterStatus === 'In progress' ? 'btn-primary' : 'btn-secondary'"
                class="text-sm"
              >
                In progress
              </button>
              <button 
                @click="filterStatus = 'Done'" 
                :class="filterStatus === 'Done' ? 'btn-primary' : 'btn-secondary'"
                class="text-sm"
              >
                Done
              </button>
            </div>
            
            <div v-if="filteredTasks.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
              Brak zadań
            </div>
            
            <div v-else class="space-y-3">
              <div 
                v-for="task in filteredTasks" 
                :key="task.id"
                class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg hover:shadow-md transition-shadow"
              >
                <div class="flex justify-between items-start mb-2">
                  <h3 class="font-semibold text-lg">{{ task.title }}</h3>
                  <div class="flex space-x-2">
                    <button 
                      @click="openEditTask(task)" 
                      class="text-primary-600 hover:text-primary-700"
                      title="Edytuj zadanie"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                      </svg>
                    </button>
                    <button 
                      @click="handleDeleteTask(task.id)" 
                      class="text-red-600 hover:text-red-700"
                      title="Usuń zadanie"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                      </svg>
                    </button>
                  </div>
                </div>
                
                <p class="text-gray-600 dark:text-gray-400 text-sm mb-3">
                  {{ task.description || 'Brak opisu' }}
                </p>
                
                <div class="flex items-center justify-between text-sm">
                  <span 
                    :class="getStatusColor(task.status)"
                    class="px-3 py-1 rounded-full font-medium"
                  >
                    {{ task.status }}
                  </span>
                  <span class="text-gray-500 dark:text-gray-400 flex items-center">
                    <svg v-if="task.assigned_to" class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                    </svg>
                    {{ task.assigned_to ? task.assigned_to.username : 'Nieprzypisane' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div 
        v-if="showInviteModal" 
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
        @click.self="showInviteModal = false"
      >
        <div class="bg-white dark:bg-gray-800 rounded-lg max-w-md w-full p-6">
          <h2 class="text-2xl font-bold mb-4">Dodaj członka</h2>
          
          <form @submit.prevent="handleInviteMember" class="space-y-4">
            <div v-if="inviteError" class="bg-red-50 dark:bg-red-900/20 border border-red-300 dark:border-red-800 text-red-800 dark:text-red-300 px-4 py-3 rounded-lg text-sm">
              {{ inviteError }}
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-2">Nazwa użytkownika</label>
              <input
                v-model="inviteUsername"
                type="text"
                required
                class="input-field"
                placeholder="Wpisz username"
              />
            </div>
            
            <div class="flex justify-end space-x-3">
              <button type="button" @click="showInviteModal = false" class="btn-secondary">
                Anuluj
              </button>
              <button type="submit" class="btn-primary">
                Dodaj
              </button>
            </div>
          </form>
        </div>
      </div>
      
      <div 
        v-if="showEditModal" 
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
        @click.self="showEditModal = false"
      >
        <div class="bg-white dark:bg-gray-800 rounded-lg max-w-md w-full p-6">
          <h2 class="text-2xl font-bold mb-4">Edytuj projekt</h2>
          
          <form @submit.prevent="handleEditProject" class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">Nazwa projektu</label>
              <input
                v-model="editData.name"
                type="text"
                required
                class="input-field"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-2">Opis</label>
              <textarea
                v-model="editData.description"
                rows="3"
                class="input-field resize-none"
              ></textarea>
            </div>
            
            <div class="flex justify-end space-x-3">
              <button type="button" @click="showEditModal = false" class="btn-secondary">
                Anuluj
              </button>
              <button type="submit" class="btn-primary">
                Zapisz
              </button>
            </div>
          </form>
        </div>
      </div>
      
      <div 
        v-if="showTaskModal" 
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
        @click.self="showTaskModal = false"
      >
        <div class="bg-white dark:bg-gray-800 rounded-lg max-w-md w-full p-6">
          <h2 class="text-2xl font-bold mb-4">{{ editingTask ? 'Edytuj zadanie' : 'Nowe zadanie' }}</h2>
          
          <form @submit.prevent="handleSaveTask" class="space-y-4">
            <div>
              <label class="block text-sm font-medium mb-2">Tytuł</label>
              <input
                v-model="taskData.title"
                type="text"
                required
                class="input-field"
                placeholder="Tytuł zadania"
              />
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-2">Opis</label>
              <textarea
                v-model="taskData.description"
                rows="3"
                class="input-field resize-none"
                placeholder="Opis zadania..."
              ></textarea>
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-2">Status</label>
              <select v-model="taskData.status" class="input-field">
                <option value="To do">To do</option>
                <option value="In progress">In progress</option>
                <option value="Done">Done</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium mb-2">Przypisz do</label>
              <select v-model="taskData.assigned_to" class="input-field">
                <option :value="null">Nieprzypisane</option>
                <option v-for="member in members" :key="member.user.id" :value="member.user.id">
                  {{ member.user.username }}
                </option>
              </select>
            </div>
            
            <div class="flex justify-end space-x-3">
              <button type="button" @click="closeTaskModal" class="btn-secondary">
                Anuluj
              </button>
              <button type="submit" class="btn-primary">
                {{ editingTask ? 'Zapisz' : 'Utwórz' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useProjectsStore } from '../stores/projects'
import { useTasksStore } from '../stores/tasks'

export default {
  name: 'ProjectDetails',
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    const projectsStore = useProjectsStore()
    const tasksStore = useTasksStore()
    
    const showInviteModal = ref(false)
    const showEditModal = ref(false)
    const showTaskModal = ref(false)
    const inviteUsername = ref('')
    const inviteError = ref('')
    const filterStatus = ref(null)
    const editingTask = ref(null)
    
    const editData = ref({
      name: '',
      description: ''
    })
    
    const taskData = ref({
      title: '',
      description: '',
      status: 'To do',
      assigned_to: null
    })
    
    const user = computed(() => authStore.user)
    const currentProject = computed(() => projectsStore.currentProject)
    const loading = computed(() => projectsStore.loading)
    const tasks = computed(() => tasksStore.tasks)
    const members = computed(() => currentProject.value?.members || [])
    const isOwner = computed(() => currentProject.value?.owner_id === user.value?.id)
    
    const filteredTasks = computed(() => {
      if (!filterStatus.value) return tasks.value
      return tasks.value.filter(t => t.status === filterStatus.value)
    })
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('pl-PL')
    }
    
    const getStatusColor = (status) => {
      const colors = {
        'To do': 'bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-200',
        'In progress': 'bg-blue-200 dark:bg-blue-900 text-blue-800 dark:text-blue-200',
        'Done': 'bg-green-200 dark:bg-green-900 text-green-800 dark:text-green-200'
      }
      return colors[status] || colors['To do']
    }
    
    const loadProject = async () => {
      const projectId = route.params.id
      await projectsStore.fetchProject(projectId)
      await tasksStore.fetchTasks(projectId)
      
      if (currentProject.value) {
        editData.value = {
          name: currentProject.value.name,
          description: currentProject.value.description || ''
        }
      }
    }
    
    const handleInviteMember = async () => {
      inviteError.value = ''
      const result = await projectsStore.inviteMember(currentProject.value.id, inviteUsername.value)
      
      if (result.success) {
        showInviteModal.value = false
        inviteUsername.value = ''
      } else {
        inviteError.value = result.error
      }
    }
    
    const handleRemoveMember = async (userId) => {
      if (!confirm('Czy na pewno chcesz usunąć tego członka?')) return
      
      await projectsStore.removeMember(currentProject.value.id, userId)
    }
    
    const handleEditProject = async () => {
      await projectsStore.updateProject(currentProject.value.id, editData.value)
      showEditModal.value = false
    }
    
    const confirmDelete = async () => {
      if (!confirm('Czy na pewno chcesz usunąć ten projekt? Operacja jest nieodwracalna.')) return
      
      const result = await projectsStore.deleteProject(currentProject.value.id)
      if (result.success) {
        router.push('/dashboard')
      }
    }
    
    const openEditTask = (task) => {
      editingTask.value = task
      taskData.value = {
        title: task.title,
        description: task.description || '',
        status: task.status,
        assigned_to: task.assigned_to?.id || null
      }
      showTaskModal.value = true
    }
    
    const closeTaskModal = () => {
      showTaskModal.value = false
      editingTask.value = null
      taskData.value = {
        title: '',
        description: '',
        status: 'To do',
        assigned_to: null
      }
    }
    
    const handleSaveTask = async () => {
      if (editingTask.value) {
        await tasksStore.updateTask(editingTask.value.id, taskData.value)
      } else {
        await tasksStore.createTask(currentProject.value.id, taskData.value)
      }
      closeTaskModal()
    }
    
    const handleDeleteTask = async (taskId) => {
      if (!confirm('Czy na pewno chcesz usunąć to zadanie?')) return
      await tasksStore.deleteTask(taskId)
    }
    
    onMounted(() => {
      loadProject()
    })
    
    watch(() => route.params.id, () => {
      if (route.params.id) {
        loadProject()
      }
    })
    
    return {
      user,
      currentProject,
      loading,
      tasks,
      members,
      isOwner,
      filteredTasks,
      showInviteModal,
      showEditModal,
      showTaskModal,
      inviteUsername,
      inviteError,
      filterStatus,
      editData,
      taskData,
      editingTask,
      formatDate,
      getStatusColor,
      handleInviteMember,
      handleRemoveMember,
      handleEditProject,
      confirmDelete,
      openEditTask,
      closeTaskModal,
      handleSaveTask,
      handleDeleteTask
    }
  }
}
</script>
