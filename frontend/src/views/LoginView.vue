<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card shadow">
          <div class="card-body p-5">
            <h3 class="text-center fw-bold mb-4">
              <i class="bi bi-shield-lock me-2"></i>Secure Login
            </h3>
            <form @submit.prevent="login">
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input type="email" class="form-control" v-model="email" required placeholder="user@example.com">
              </div>
              <div class="mb-4">
                <label class="form-label">Password</label>
                <input type="password" class="form-control" v-model="password" required placeholder="Enter password">
              </div>
              <button type="submit" class="btn btn-primary w-100 btn-lg" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                {{ loading ? 'Authenticating...' : 'Login' }}
              </button>
            </form>
            <div class="text-center mt-4">
              <small class="text-muted">
                <i class="bi bi-info-circle me-1"></i>
                Authentication secured via Azure Key Vault JWT secrets
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useAuthStore } from '../store/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'LoginView',
  setup() {
    const email = ref('')
    const password = ref('')
    const loading = ref(false)
    const authStore = useAuthStore()
    const router = useRouter()

    const login = async () => {
      loading.value = true
      try {
        await authStore.login(email.value, password.value)
        router.push('/')
      } catch (error) {
        alert('Login failed: ' + error.message)
      } finally {
        loading.value = false
      }
    }

    return { email, password, loading, login }
  }
}
</script>
