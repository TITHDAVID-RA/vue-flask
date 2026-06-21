<template>
  <div class="container my-5">
    <h2 class="mb-4 fw-bold">
      <i class="bi bi-cart3 me-2"></i>Shopping Cart
    </h2>

    <div v-if="cartStore.items.length === 0" class="text-center py-5">
      <i class="bi bi-cart-x display-1 text-muted"></i>
      <h4 class="mt-3 text-muted">Your cart is empty</h4>
      <router-link to="/products" class="btn btn-primary mt-3">
        Continue Shopping
      </router-link>
    </div>

    <div v-else class="row">
      <div class="col-lg-8">
        <div class="card">
          <div class="card-body">
            <div v-for="item in cartStore.items" :key="item.id" class="d-flex align-items-center mb-3 pb-3 border-bottom">
              <img :src="item.image_url" class="rounded" style="width: 80px; height: 80px; object-fit: cover;" :alt="item.name">
              <div class="ms-3 flex-grow-1">
                <h5 class="mb-1">{{ item.name }}</h5>
                <p class="text-muted mb-0">${{ item.price.toFixed(2) }}</p>
              </div>
              <div class="d-flex align-items-center">
                <button @click="cartStore.updateQuantity(item.id, item.quantity - 1)" class="btn btn-outline-secondary btn-sm">-</button>
                <span class="mx-3">{{ item.quantity }}</span>
                <button @click="cartStore.updateQuantity(item.id, item.quantity + 1)" class="btn btn-outline-secondary btn-sm">+</button>
              </div>
              <div class="ms-4 text-end" style="min-width: 100px;">
                <p class="fw-bold mb-0">${{ (item.price * item.quantity).toFixed(2) }}</p>
                <button @click="cartStore.removeItem(item.id)" class="btn btn-link text-danger btn-sm p-0">
                  <i class="bi bi-trash"></i> Remove
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-lg-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title fw-bold">Order Summary</h5>
            <hr>
            <div class="d-flex justify-content-between mb-2">
              <span>Subtotal</span>
              <span>${{ cartStore.subtotal.toFixed(2) }}</span>
            </div>
            <div class="d-flex justify-content-between mb-2">
              <span>Tax (8%)</span>
              <span>${{ cartStore.tax.toFixed(2) }}</span>
            </div>
            <div class="d-flex justify-content-between mb-3">
              <span>Shipping</span>
              <span class="text-success">Free</span>
            </div>
            <hr>
            <div class="d-flex justify-content-between mb-4">
              <span class="fw-bold">Total</span>
              <span class="fw-bold fs-5">${{ cartStore.total.toFixed(2) }}</span>
            </div>
            <button @click="proceedToCheckout" class="btn btn-primary w-100 btn-lg">
              <i class="bi bi-lock-fill me-2"></i>Secure Checkout
            </button>
            <div class="text-center mt-3">
              <small class="text-muted">
                <i class="bi bi-shield-check me-1"></i>
                Secured by Azure Key Vault
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useCartStore } from '../store/cart'
import { useRouter } from 'vue-router'

export default {
  name: 'CartView',
  setup() {
    const cartStore = useCartStore()
    const router = useRouter()

    const proceedToCheckout = () => {
      router.push('/checkout')
    }

    return { cartStore, proceedToCheckout }
  }
}
</script>
