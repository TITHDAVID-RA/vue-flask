<template>
  <div class="card h-100">
    <div class="position-relative">
      <img :src="product.image_url" class="card-img-top" :alt="product.name" style="height: 220px; object-fit: cover;">
      <span v-if="product.featured" class="badge bg-warning position-absolute top-0 end-0 m-2">Featured</span>
    </div>
    <div class="card-body d-flex flex-column">
      <h5 class="card-title">{{ product.name }}</h5>
      <p class="card-text text-muted small flex-grow-1">{{ product.description }}</p>
      <div class="d-flex justify-content-between align-items-center mt-3">
        <span class="h5 mb-0 text-primary">${{ product.price.toFixed(2) }}</span>
        <button @click="addToCart" class="btn btn-primary">
          <i class="bi bi-cart-plus me-1"></i>Add to Cart
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useCartStore } from '../store/cart'

export default {
  name: 'ProductCard',
  props: {
    product: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const cartStore = useCartStore()

    const addToCart = () => {
      cartStore.addItem(props.product)
    }

    return { addToCart }
  }
}
</script>
