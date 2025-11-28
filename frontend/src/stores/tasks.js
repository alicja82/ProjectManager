import { defineStore } from 'pinia'
import { ref } from 'vue'
import { tasksAPI } from '../api'

export const useTasksStore = defineStore('tasks', () => {
  const tasks = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchTasks(projectId, filters = {}) {
    loading.value = true
    error.value = null
    
    try {
      const response = await tasksAPI.getAll(projectId, filters)
      tasks.value = response.data.tasks
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Błąd pobierania zadań'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function createTask(projectId, data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await tasksAPI.create(projectId, data)
      tasks.value.unshift(response.data.task)
      return { success: true, data: response.data.task }
    } catch (err) {
      error.value = err.response?.data?.error || 'Błąd tworzenia zadania'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function updateTask(id, data) {
    loading.value = true
    error.value = null
    
    try {
      const response = await tasksAPI.update(id, data)
      const index = tasks.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tasks.value[index] = response.data.task
      }
      return { success: true, data: response.data.task }
    } catch (err) {
      error.value = err.response?.data?.error || 'Błąd aktualizacji zadania'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function deleteTask(id) {
    loading.value = true
    error.value = null
    
    try {
      await tasksAPI.delete(id)
      tasks.value = tasks.value.filter(t => t.id !== id)
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error || 'Błąd usuwania zadania'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  function clearTasks() {
    tasks.value = []
  }

  return {
    tasks,
    loading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    clearTasks
  }
})
