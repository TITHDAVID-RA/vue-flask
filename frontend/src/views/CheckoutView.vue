<template>
  <div class="container my-5">
    <h2 class="mb-4 fw-bold">
      <i class="bi bi-credit-card me-2"></i>Secure Checkout
    </h2>

    <div class="row">
      <div class="col-lg-8">
        <div class="card mb-4">
          <div class="card-body">
            <h5 class="card-title fw-bold mb-4">Shipping Information</h5>
            <form @submit.prevent="submitOrder">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">First Name</label>
                  <input type="text" class="form-control" v-model="shipping.firstName" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Last Name</label>
                  <input type="text" class="form-control" v-model="shipping.lastName" required>
                </div>
                <div class="col-12">
                  <label class="form-label">Email</label>
                  <input type="email" class="form-control" v-model="shipping.email" required>
                </div>
                <div class="col-12">
                  <label class="form-label">Address</label>
                  <input type="text" class="form-control" v-model="shipping.address" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">City</label>
                  <input type="text" class="form-control" v-model="shipping.city" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">State</label>
                  <input type="text" class="form-control" v-model="shipping.state" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">ZIP</label>
                  <input type="text" class="form-control" v-model="shipping.zip" required>
                </div>
              </div>

              <hr class="my-4">

              <h5 class="card-title fw-bold mb-4">Payment Information</h5>
              <div class="alert alert-info">
                <i class="bi bi-info-circle-fill me-2"></i>
                <strong>Secure Payment:</strong> Your payment is processed using Stripe API keys securely retrieved from Azure Key Vault at runtime. No payment secrets are ever stored in code or configuration files.
              </div>

              <div id="card-element" class="form-control py-3 mb-3"></div>
              <div id="card-errors" class="text-danger mb-3" role="alert"></div>

              <button type="submit" class="btn btn-primary btn-lg w-100" :disabled="processing">
                <span v-if="processing">
                  <span class="spinner-border spinner-border-sm me-2"></span>
                  Processing...
                </span>
                <span v-else>
                  <i class="bi bi-lock-fill me-2"></i>
                  Pay ${{ cartStore.total.toFixed(2) }}
                </span>
              </button>
            </form>
          </div>
        </div>
      </div>

      <div class="col-lg-4">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title fw-bold">Order Summary</h5>
            <hr>
            <div v-for="item in cartStore.items" :key="item.id" class="d-flex justify-content-between mb-2">
              <span>{{ item.name }} x{{ item.quantity }}</span>
              <span>${{ (item.price * item.quantity).toFixed(2) }}</span>
            </div>
            <hr>
            <div class="d-flex justify-content-between mb-2">
              <span>Subtotal</span>
              <span>${{ cartStore.subtotal.toFixed(2) }}</span>
            </div>
            <div class="d-flex justify-content-between mb-2">
              <span>Tax</span>
              <span>${{ cartStore.tax.toFixed(2) }}</span>
            </div>
            <hr>
            <div class="d-flex justify-content-between">
              <span class="fw-bold">Total</span>
              <span class="fw-bold fs-5">${{ cartStore.total.toFixed(2) }}</span>
            </div>
          </div>
        </div>

        <div class="card mt-3 border-success">
          <div class="card-body">
            <h6 class="fw-bold text-success">
              <i class="bi bi-shield-lock me-2"></i>Security Details
            </h6>
            <ul class="list-unstyled small text-muted mb-0">
              <li><i class="bi bi-check-circle-fill text-success me-2"></i>Azure Key Vault protected</li>
              <li><i class="bi bi-check-circle-fill text-success me-2"></i>Managed Identity auth</li>
              <li><i class="bi bi-check-circle-fill text-success me-2"></i>TLS 1.3 encrypted</li>
              <li><i class="bi bi-check-circle-fill text-success me-2"></i>PCI-DSS compliant</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { loadStripe } from '@stripe/stripe-js'
import { useCartStore } from '../store/cart'
import { useRouter } from 'vue-router'
import api from '../services/api'

export default {
  name: 'CheckoutView',
  setup() {
    const cartStore = useCartStore()
    const router = useRouter()
    const processing = ref(false)
    const shipping = ref({
      firstName: '',
      lastName: '',
      email: '',
      address: '',
      city: '',
      state: '',
      zip: ''
    })

    let stripe = null
    let cardElement = null

    onMounted(async () => {
      try {
        // Get Stripe publishable key from backend (retrieved from Key Vault)
        const response = await api.get('/config/stripe-key')
        stripe = await loadStripe(response.data.publishable_key)

        const elements = stripe.elements()
        cardElement = elements.create('card', {
          style: {
            base: {
              fontSize: '16px',
              color: '#424770',
              '::placeholder': { color: '#aab7c4' }
            }
          }
        })
        cardElement.mount('#card-element')
      } catch (error) {
        console.error('Failed to initialize Stripe:', error)
      }
    })

    const submitOrder = async () => {
      if (cartStore.items.length === 0) return

      processing.value = true
      try {
        const { error, paymentMethod } = await stripe.createPaymentMethod({
          type: 'card',
          card: cardElement,
          billing_details: {
            name: `${shipping.value.firstName} ${shipping.value.lastName}`,
            email: shipping.value.email
          }
        })

        if (error) {
          document.getElementById('card-errors').textContent = error.message
          processing.value = false
          return
        }

        const orderData = {
          shipping: shipping.value,
          items: cartStore.items,
          payment_method_id: paymentMethod.id,
          total: cartStore.total
        }

        const response = await api.post('/orders', orderData)

        if (response.data.success) {
          cartStore.clearCart()
          router.push('/order-success')
        }
      } catch (error) {
        console.error('Order failed:', error)
        document.getElementById('card-errors').textContent = 'Payment processing failed. Please try again.'
      } finally {
        processing.value = false
      }
    }

    return { shipping, cartStore, processing, submitOrder }
  }
}
</script>
