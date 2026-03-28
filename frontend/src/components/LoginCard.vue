<template>
  <div class="login-card">
    <img :src="logo42" alt="42 logo" class="logo-image" />
    <h1 class="title">Sign in</h1>
    <p class="subtitle">Choose your authentication provider</p>

    <div class="buttons">
      <button @click="$emit('login-42')" class="login-btn primary">
        Login with 42 Intra
      </button>

      <button @click="$emit('login-learninghub')" class="login-btn secondary">
        Login with Learning Hub
      </button>
    </div>
  </div>
</template>

<script>
import logo42 from '../assets/42.png'

export default {
  data() {
    return {
      logo42
    }
  }
}
</script>

<style scoped>
.login-card {
  width: 100%;
  max-width: 420px;
  padding: 32px 24px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(18px);
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
  animation: float 5s ease-in-out infinite;
}

.logo-image {
  width: 72px;
  height: 72px;
  object-fit: contain;
  display: block;
  margin: 0 auto 20px;
}

.title {
  margin: 0;
  font-size: 2rem;
  font-weight: 800;
  color: white;
}

.subtitle {
  margin-top: 10px;
  margin-bottom: 28px;
  color: #cbd5e1;
}

.buttons {
  display: grid;
  gap: 14px;
}

.login-btn {
  width: 100%;
  padding: 15px 18px;
  border: none;
  border-radius: 16px;
  color: white;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.login-btn:hover {
  transform: translateY(-2px) scale(1.02);
}

.primary {
  background: linear-gradient(90deg, #6366f1, #22d3ee);
  box-shadow: 0 12px 30px rgba(34, 211, 238, 0.25);
}

.secondary {
  background: linear-gradient(90deg, #0f766e, #14b8a6);
  box-shadow: 0 12px 30px rgba(20, 184, 166, 0.25);
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-8px); }
  100% { transform: translateY(0px); }
}
</style>