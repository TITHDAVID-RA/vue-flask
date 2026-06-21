<template>
  <div class="container my-5">
    <h2 class="mb-4 fw-bold">All Products</h2>
    <div class="row g-4">
      <div v-for="product in products" :key="product.id" class="col-md-4 col-lg-3">
        <ProductCard :product="product" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import ProductCard from '../components/ProductCard.vue'
import api from '../services/api'

export default {
  name: 'ProductsView',
  components: {
    ProductCard
  },
  setup() {
    const products = ref([])

    onMounted(async () => {
      try {
        const response = await api.get('/products')
        products.value = response.data
      } catch (error) {
        console.error('Failed to load products:', error)
        products.value = [
          {
            id: 1,
            name: 'Wireless Headphones Pro',
            description: 'Premium noise-cancelling wireless headphones with 30-hour battery life.',
            price: 249.99,
            image_url: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400',
            featured: true
          },
          {
            id: 2,
            name: 'Smart Watch Ultra',
            description: 'Advanced fitness tracking with GPS, heart rate monitor, and 7-day battery.',
            price: 399.99,
            image_url: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400',
            featured: true
          },
          {
            id: 3,
            name: '4K Webcam Studio',
            description: 'Professional 4K webcam with auto-focus and built-in ring light.',
            price: 179.99,
            image_url: 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=400',
            featured: true
          },
          {
            id: 4,
            name: 'Mechanical Keyboard RGB',
            description: 'Hot-swappable mechanical keyboard with per-key RGB lighting.',
            price: 149.99,
            image_url: 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400',
            featured: false
          },
          {
            id: 5,
            name: 'Portable SSD 2TB',
            description: 'Ultra-fast NVMe portable SSD with USB-C connectivity.',
            price: 199.99,
            image_url: 'https://images.unsplash.com/photo-1597872252165-4827a235d7bc?w=400',
            featured: false
          },
          {
            id: 6,
            name: 'USB-C Docking Station',
            description: '12-in-1 USB-C docking station with dual 4K HDMI output.',
            price: 129.99,
            image_url: 'https://images.unsplash.com/photo-1625772299848-391b6a87d7b3?w=400',
            featured: false
          }
        ]
      }
    })

    return { products }
  }
}
</script>
