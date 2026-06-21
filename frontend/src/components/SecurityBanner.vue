<template>
  <div class="security-banner mb-4">
    <div class="container">
      <div class="row align-items-center">
        <div class="col-md-6">
          <div class="security-content">
            <div class="d-flex align-items-center mb-3">
              <div class="check-icon me-3">
                <i class="bi bi-check-circle-fill"></i>
              </div>
              <h3 class="mb-0 fw-bold">How IT WORKS</h3>
            </div>
            <ol class="security-steps">
              <li>User access the SaaS application.</li>
              <li>The application is hosted on Azure App Service.</li>
              <li>App Service uses Managed Identity to authenticate to Azure Key Vault.</li>
              <li>Key Vault returns the payment API secret securely.</li>
              <li>The secret is used by the application at runtime. It is never stored in code or configuration.</li>
            </ol>
          </div>
        </div>
        <div class="col-md-6">
          <div class="security-diagram text-center">
            <div class="diagram-flow">
              <div class="diagram-node user-node">
                <i class="bi bi-person-circle"></i>
                <span>User</span>
              </div>
              <div class="diagram-arrow"><i class="bi bi-arrow-down"></i></div>
              <div class="diagram-node app-node">
                <i class="bi bi-window"></i>
                <span>Azure App Service</span>
              </div>
              <div class="diagram-arrow"><i class="bi bi-arrow-down"></i></div>
              <div class="diagram-node vault-node">
                <i class="bi bi-shield-lock"></i>
                <span>Azure Key Vault</span>
              </div>
              <div class="diagram-arrow"><i class="bi bi-arrow-down"></i></div>
              <div class="diagram-node secret-node">
                <i class="bi bi-key"></i>
                <span>Secure Secret</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SecurityBanner'
}
</script>

<style scoped>
.security-banner {
  background: linear-gradient(135deg, #0a1628 0%, #1a2744 50%, #0d1b2a 100%);
  color: white;
  padding: 50px 0;
  border-radius: 0;
}

.check-icon {
  width: 40px;
  height: 40px;
  background: #4a90d9;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.check-icon i {
  font-size: 20px;
  color: white;
}

.security-steps {
  list-style: none;
  counter-reset: step-counter;
  padding-left: 0;
}

.security-steps li {
  counter-increment: step-counter;
  padding: 10px 0 10px 45px;
  position: relative;
  font-size: 15px;
  line-height: 1.6;
  color: #c8d6e5;
}

.security-steps li::before {
  content: counter(step-counter) ".";
  position: absolute;
  left: 0;
  font-weight: bold;
  color: #4a90d9;
  font-size: 18px;
}

.diagram-flow {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.diagram-node {
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 12px;
  padding: 15px 25px;
  display: flex;
  align-items: center;
  gap: 12px;
  width: 220px;
  justify-content: center;
  transition: all 0.3s;
}

.diagram-node:hover {
  background: rgba(255,255,255,0.2);
  transform: scale(1.05);
}

.diagram-node i {
  font-size: 24px;
}

.user-node i { color: #74b9ff; }
.app-node i { color: #00cec9; }
.vault-node i { color: #fdcb6e; }
.secret-node i { color: #55efc4; }

.diagram-arrow {
  color: rgba(255,255,255,0.5);
  font-size: 20px;
}

.diagram-arrow i {
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-5px); }
  60% { transform: translateY(-3px); }
}
</style>
