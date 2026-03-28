<template>
  <div style="font-family: Arial; padding: 2rem; max-width: 700px; margin: auto;">
    <div v-if="page === 'login'">
      <h1>Login</h1>
      <p>Sign in with your 42 intra account.</p>
      <button @click="loginWith42" style="padding: 0.8rem 1.2rem; cursor: pointer;">
        Login with 42
      </button>
    </div>

    <div v-else-if="page === 'auth-success'">
      <h1>Logging you in...</h1>
      <p>Please wait.</p>
    </div>

    <div v-else-if="page === 'profile'">
      <h1>Welcome {{ user.display_name || user.login }}</h1>
      <img
        v-if="user.image_url"
        :src="user.image_url"
        alt="avatar"
        width="120"
        style="border-radius: 50%; margin-bottom: 1rem;"
      />
      <pre>{{ user }}</pre>
      <button @click="logout" style="padding: 0.8rem 1.2rem; cursor: pointer;">
        Logout
      </button>
    </div>

    <div v-else>
      <h1>Page not found</h1>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      page: 'login',
      user: null
    }
  },
  async mounted() {
    const path = window.location.pathname

    if (path === '/' || path === '/login') {
      this.page = 'login'
    } else if (path === '/auth-success') {
      this.page = 'auth-success'
      const params = new URLSearchParams(window.location.search)
      const token = params.get('token')

      if (token) {
        localStorage.setItem('token', token)
        window.history.replaceState({}, document.title, '/profile')
        await this.loadProfile()
      } else {
        this.page = 'login'
      }
    } else if (path === '/profile') {
      await this.loadProfile()
    } else {
      this.page = 'not-found'
    }
  },
  methods: {
    loginWith42() {
      window.location.href = 'http://localhost:5000/auth/42/login'
    },
    async loadProfile() {
      const token = localStorage.getItem('token')
      if (!token) {
        this.page = 'login'
        return
      }

      try {
        const res = await fetch('http://localhost:5000/me', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        if (!res.ok) {
          throw new Error('Unauthorized')
        }

        this.user = await res.json()
        this.page = 'profile'
      } catch (e) {
        localStorage.removeItem('token')
        this.page = 'login'
      }
    },
    logout() {
      localStorage.removeItem('token')
      this.user = null
      window.history.replaceState({}, document.title, '/login')
      this.page = 'login'
    }
  }
}
</script>