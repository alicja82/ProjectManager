import api from './axios'

// Autoryzacja
export const authAPI = {
  register(data) {
    return api.post('/register', data)
  },
  login(data) {
    return api.post('/login', data)
  },
  getCurrentUser() {
    return api.get('/me')
  }
}

// Projekty
export const projectsAPI = {
  getAll() {
    return api.get('/projects')
  },
  getById(id) {
    return api.get(`/projects/${id}`)
  },
  create(data) {
    return api.post('/projects', data)
  },
  update(id, data) {
    return api.put(`/projects/${id}`, data)
  },
  delete(id) {
    return api.delete(`/projects/${id}`)
  },
  inviteMember(projectId, username) {
    return api.post(`/projects/${projectId}/invite`, { username })
  },
  removeMember(projectId, userId) {
    return api.delete(`/projects/${projectId}/members/${userId}`)
  }
}

// Zadania
export const tasksAPI = {
  getAll(projectId, filters = {}) {
    return api.get(`/projects/${projectId}/tasks`, { params: filters })
  },
  getById(id) {
    return api.get(`/tasks/${id}`)
  },
  create(projectId, data) {
    return api.post(`/projects/${projectId}/tasks`, data)
  },
  update(id, data) {
    return api.put(`/tasks/${id}`, data)
  },
  delete(id) {
    return api.delete(`/tasks/${id}`)
  }
}
