<template>
  <div class="page">
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    <div class="blob blob-3"></div>

    <div class="login-wrapper" v-if="page === 'login'">
      <div class="login-card">
        <img :src="logo42" alt="42 logo" class="logo-image" />

        <h1 class="title">Sign in</h1>
        <p class="subtitle">Continue with your 42 Intra account</p>

        <button @click="loginWith42" class="login-btn">
          Login with 42 Intra
        </button>
      </div>
    </div>

    <div class="login-wrapper" v-else-if="page === 'loading'">
      <div class="login-card">
        <div class="spinner"></div>
        <h1 class="title">Logging in...</h1>
        <p class="subtitle">Please wait while we verify your account</p>
      </div>
    </div>

    <div class="login-wrapper" v-else-if="page === 'profile'">
      <div class="login-card">
        <img v-if="user && user.image_url" :src="user.image_url" alt="avatar" class="avatar" />
        <img v-else :src="logo42" alt="42 logo" class="logo-image" />

        <h1 class="title">{{ user?.display_name || user?.login }}</h1>
        <p class="subtitle">@{{ user?.login }}</p>

        <button @click="logout" class="login-btn">
          Logout
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import logo42 from './assets/42.png'

const API_URL = 'http://localhost:5000'

export default {
  data() {
    return {
      logo42,
      page: 'login',
      user: null
    }
  },
  async mounted() {
    const params = new URLSearchParams(window.location.search)
    const token = params.get('token')
    const savedToken = localStorage.getItem('token')

    if (token) {
      localStorage.setItem('token', token)
      window.history.replaceState({}, document.title, '/')
      await this.loadProfile()
      return
    }

    if (savedToken) {
      await this.loadProfile()
    }
  },
  methods: {
    loginWith42() {
      window.location.href = `${API_URL}/auth/42/login`
    },
    async loadProfile() {
      const token = localStorage.getItem('token')
      if (!token) {
        this.page = 'login'
        return
      }

      this.page = 'loading'

      try {
        const res = await fetch(`${API_URL}/me`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        if (!res.ok) {
          throw new Error('Unauthorized')
        }

        this.user = await res.json()
        this.page = 'profile'
      } catch (error) {
        localStorage.removeItem('token')
        this.user = null
        this.page = 'login'
      }
    },
    logout() {
      localStorage.removeItem('token')
      this.user = null
      this.page = 'login'
    }
  }
}
</script>

<style scoped>
.page {
  position: relative;
  min-height: 100vh;
  overflow: hidden;
  background: linear-gradient(135deg, #020617 0%, #0f172a 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  font-family: 'Inter', Arial, sans-serif;
}

.login-wrapper {
  position: relative;
  z-index: 2;
  width: 100%;
  display: flex;
  justify-content: center;
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 32px 24px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
  text-align: center;
  animation: float 5s ease-in-out infinite;
}

.logo-image,
.avatar {
  width: 72px;
  height: 72px;
  object-fit: contain;
  display: block;
  margin: 0 auto 20px;
  border-radius: 50%;
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
  font-size: 0.95rem;
  color: #cbd5e1;
  line-height: 1.5;
}

.login-btn {
  width: 100%;
  padding: 15px 18px;
  border: none;
  border-radius: 16px;
  background: linear-gradient(90deg, #6366f1, #22d3ee);
  color: white;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  box-shadow: 0 12px 30px rgba(34, 211, 238, 0.25);
}

.login-btn:hover {
  transform: translateY(-2px) scale(1.02);
  box-shadow: 0 18px 35px rgba(34, 211, 238, 0.35);
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

.blob {
  position: absolute;
  border-radius: 9999px;
  filter: blur(80px);
  opacity: 0.45;
  animation: blobMove 10s infinite ease-in-out;
}

.blob-1 {
  width: 220px;
  height: 220px;
  background: #6366f1;
  top: 8%;
  left: 5%;
}

.blob-2 {
  width: 260px;
  height: 260px;
  background: #22d3ee;
  bottom: 8%;
  right: 5%;
  animation-delay: 2s;
}

.blob-3 {
  width: 180px;
  height: 180px;
  background: #0ea5e9;
  top: 55%;
  left: 40%;
  animation-delay: 4s;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-8px); }
  100% { transform: translateY(0px); }
}

@keyframes blobMove {
  0% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -20px) scale(1.08); }
  66% { transform: translate(-20px, 20px) scale(0.95); }
  100% { transform: translate(0, 0) scale(1); }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 640px) {
  .login-card {
    max-width: 100%;
    padding: 28px 20px;
    border-radius: 24px;
  }

  .logo-image,
  .avatar {
    width: 64px;
    height: 64px;
    margin-bottom: 18px;
  }

  .title {
    font-size: 1.75rem;
  }

  .subtitle {
    font-size: 0.9rem;
    margin-bottom: 24px;
  }

  .login-btn {
    padding: 14px 16px;
    font-size: 0.95rem;
  }
}
</style>