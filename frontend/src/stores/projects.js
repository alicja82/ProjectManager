import { defineStore } from 'pinia'
import { ref } from 'vue'
import { projectsAPI } from '../api'

export const useProjectsStore = defineStore('projects', () => {
  const projects = ref([])
  const currentProject = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function fetchProjects() {
    loading.value = true
    error.value = null
    
    try {
      const response = await projectsAPI.getAll()
      projects.value = response.data.projects
      return { success: true }
    } catch (err) {
      // Optional chaining - err.response może nie istnieć przy błędach sieciowych
      error.value = err.response?.data?.error || 'Błąd pobierania projektów'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function fetchProject(id) {
    loading.value = true
    error.value = null
    
    try {
      const response = await projectsAPI.getById(id)
      currentProject.value = response.data.project
      return { success: true, data: response.data.project }
    } catch (err) {
      error.value = err.response?.data?.error || 'Błąd pobierania projektu'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function createProject(data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await projectsAPI.create(data)
      projects.value.push(response.data.project)
      return { success: true, data: response.data.project }
    } catch (err) {
      error.value = err.response?.data?.error || 'Błąd tworzenia projektu'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function updateProject(id, data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await projectsAPI.update(id, data)
      // Synchronizacja state - aktualizuj zarówno listę jak i currentProject jeśli otwarty
      const index = projects.value.findIndex(p => p.id === id)
      if (index !== -1) {
        projects.value[index] = response.data.project
      }
      if (currentProject.value?.id === id) {
        currentProject.value = response.data.project
      }
      return { success: true, data: response.data.project }
    } catch (err) {
      error.value = err.response?.data?.error || 'Błąd aktualizacji projektu'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function deleteProject(id) {
    loading.value = true
    error.value = null
    
    try {
      await projectsAPI.delete(id)
      projects.value = projects.value.filter(p => p.id !== id)
      if (currentProject.value?.id === id) {
        currentProject.value = null
      }
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Błąd usuwania projektu'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function inviteMember(projectId, username) {
    loading.value = true
    error.value = null
    
    try {
      const response = await projectsAPI.inviteMember(projectId, username)
      // Ponowne pobranie projektu aby zaktualizować listę członków w UI
      await fetchProject(projectId)
      return { success: true, data: response.data.member }
    } catch (err) {
      error.value = err.response?.data?.error || 'Błąd dodawania członka'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function removeMember(projectId, userId) {
    loading.value = true
    error.value = null
    
    try {
      await projectsAPI.removeMember(projectId, userId)
      await fetchProject(projectId)
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Błąd usuwania członka'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  return {
    projects,
    currentProject,
    loading,
    error,
    fetchProjects,
    fetchProject,
    createProject,
    updateProject,
    deleteProject,
    inviteMember,
    removeMember
  }
})
