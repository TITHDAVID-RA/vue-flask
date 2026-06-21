<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-6 text-center">
        <div class="success-animation mb-4">
          <i class="bi bi-check-circle-fill text-success display-1"></i>
        </div>
        <h2 class="fw-bold mb-3">Order Placed Successfully!</h2>
        <p class="text-muted mb-4">
          Your payment was processed securely using Stripe API keys retrieved from Azure Key Vault.
          No secrets were ever exposed in code or configuration.
        </p>
        <div class="alert alert-success">
          <i class="bi bi-shield-check me-2"></i>
          <strong>Security Verified:</strong> Payment API secret was retrieved at runtime via Managed Identity authentication to Azure Key Vault.
        </div>
        <router-link to="/products" class="btn btn-primary btn-lg mt-3">
          <i class="bi bi-shop me-2"></i>Continue Shopping
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrderSuccessView'
}
</script>
