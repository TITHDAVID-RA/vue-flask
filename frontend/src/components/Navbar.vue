<template>
  <nav class="navbar navbar-expand-lg navbar-dark" style="background-color: var(--primary-color);">
    <div class="container">
      <router-link class="navbar-brand fw-bold" to="/">
        <i class="bi bi-shield-lock-fill me-2"></i>SecureShop
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/products">Products</router-link>
          </li>
        </ul>
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link position-relative" to="/cart">
              <i class="bi bi-cart3 fs-5"></i>
              <span v-if="cartStore.itemCount > 0" class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                {{ cartStore.itemCount }}
              </span>
            </router-link>
          </li>
          <li class="nav-item ms-3" v-if="!authStore.isAuthenticated">
            <router-link class="btn btn-outline-light btn-sm" to="/login">Login</router-link>
          </li>
          <li class="nav-item ms-3" v-else>
            <span class="nav-link">Welcome, {{ authStore.user?.name }}</span>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { useCartStore } from '../store/cart'
import { useAuthStore } from '../store/auth'

export default {
  name: 'Navbar',
  setup() {
    const cartStore = useCartStore()
    const authStore = useAuthStore()
    return { cartStore, authStore }
  }
}
</script>
