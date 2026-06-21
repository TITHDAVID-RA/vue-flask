<template>
  <div>
    <!-- Hero Section -->
    <div class="hero-section">
      <div class="container text-center py-5">
        <h1 class="display-4 fw-bold mb-3">Secure E-Commerce</h1>
        <p class="lead mb-4">Enterprise-grade shopping with Azure Key Vault security</p>
        <router-link to="/products" class="btn btn-primary btn-lg px-5">
          <i class="bi bi-shop me-2"></i>Shop Now
        </router-link>
      </div>
    </div>

    <!-- Security Banner (matches user's screenshot) -->
    <SecurityBanner />

    <!-- Featured Products -->
    <div class="container my-5">
      <h2 class="text-center mb-4 fw-bold">Featured Products</h2>
      <div class="row g-4">
        <div v-for="product in featuredProducts" :key="product.id" class="col-md-4">
          <ProductCard :product="product" />
        </div>
      </div>
    </div>

    <!-- Security Features -->
    <div class="bg-light py-5">
      <div class="container">
        <h2 class="text-center mb-5 fw-bold">Security Architecture</h2>
        <div class="row g-4">
          <div class="col-md-4 text-center">
            <div class="security-feature">
              <div class="feature-icon mb-3">
                <i class="bi bi-shield-lock"></i>
              </div>
              <h4>Azure Key Vault</h4>
              <p class="text-muted">Centralized secret management with HSM-backed encryption for maximum security.</p>
            </div>
          </div>
          <div class="col-md-4 text-center">
            <div class="security-feature">
              <div class="feature-icon mb-3">
                <i class="bi bi-fingerprint"></i>
              </div>
              <h4>Managed Identity</h4>
              <p class="text-muted">Passwordless authentication between App Service and Key Vault - no secrets in code.</p>
            </div>
          </div>
          <div class="col-md-4 text-center">
            <div class="security-feature">
              <div class="feature-icon mb-3">
                <i class="bi bi-credit-card-2-front"></i>
              </div>
              <h4>Payment Security</h4>
              <p class="text-muted">Payment API secrets retrieved securely at runtime, never stored in configuration.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import ProductCard from '../components/ProductCard.vue'
import SecurityBanner from '../components/SecurityBanner.vue'
import api from '../services/api'

export default {
  name: 'HomeView',
  components: {
    ProductCard,
    SecurityBanner
  },
  setup() {
    const featuredProducts = ref([])

    onMounted(async () => {
      try {
        const response = await api.get('/products?featured=true')
        featuredProducts.value = response.data
      } catch (error) {
        console.error('Failed to load products:', error)
        // Fallback demo data
        featuredProducts.value = [
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
          }
        ]
      }
    })

    return { featuredProducts }
  }
}
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 100%);
  color: white;
  padding: 80px 0;
}

.security-feature {
  padding: 30px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.06);
  height: 100%;
  transition: transform 0.3s;
}

.security-feature:hover {
  transform: translateY(-5px);
}

.feature-icon {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #415a77, #778da9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.feature-icon i {
  font-size: 32px;
  color: white;
}
</style>
