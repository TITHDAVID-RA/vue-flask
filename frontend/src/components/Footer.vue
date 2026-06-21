<template>
  <footer class="text-white py-4 mt-5" style="background-color: var(--primary-color);">
    <div class="container">
      <div class="row">
        <div class="col-md-4">
          <h5><i class="bi bi-shield-lock-fill me-2"></i>SecureShop</h5>
          <p class="text-muted">Enterprise-grade e-commerce with Azure Key Vault security.</p>
        </div>
        <div class="col-md-4">
          <h5>Security</h5>
          <ul class="list-unstyled text-muted">
            <li><i class="bi bi-check-circle-fill text-success me-2"></i>Azure Key Vault</li>
            <li><i class="bi bi-check-circle-fill text-success me-2"></i>Managed Identity</li>
            <li><i class="bi bi-check-circle-fill text-success me-2"></i>Encrypted Secrets</li>
            <li><i class="bi bi-check-circle-fill text-success me-2"></i>TLS/SSL Certificates</li>
          </ul>
        </div>
        <div class="col-md-4">
          <h5>How It Works</h5>
          <ol class="text-muted small">
            <li>User accesses the SaaS application</li>
            <li>Application hosted on Azure App Service</li>
            <li>App Service uses Managed Identity</li>
            <li>Key Vault returns secrets securely</li>
            <li>Secrets used at runtime, never in code</li>
          </ol>
        </div>
      </div>
      <hr class="border-secondary">
      <div class="text-center text-muted">
        <small>&copy; 2026 SecureShop. Powered by Azure Key Vault.</small>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>
