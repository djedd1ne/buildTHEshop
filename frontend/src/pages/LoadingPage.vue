<template>
  <div class="centered">
    <div class="loading-card">
      <div class="spinner"></div>
      <h1>Logging in...</h1>
      <p>Please wait while we verify your account</p>
    </div>
  </div>
</template>

<style scoped>
.centered {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  z-index: 2;
}

.loading-card {
  width: 100%;
  max-width: 400px;
  padding: 32px 24px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(18px);
  text-align: center;
  color: white;
}

.loading-card p {
  color: #cbd5e1;
}

.spinner {
  width: 48px;
  height: 48px;
  margin: 0 auto 20px;
  border: 4px solid rgba(255, 255, 255, 0.2);
  border-top: 4px solid #22d3ee;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>