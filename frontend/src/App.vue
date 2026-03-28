<template>
  <div class="page">
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    <div class="blob blob-3"></div>

    <LoginPage
      v-if="page === 'login'"
      @login-42="handleLogin42"
      @login-learninghub="handleLoginLearningHub"
    />

    <LoadingPage v-else-if="page === 'loading'" />

    <ShopPage
      v-else-if="page === 'shop'"
      :user="user"
      :balance="userBalance"
      :showProfileMenu="showProfileMenu"
      :categories="categories"
      :selectedCategory="selectedCategory"
      :products="filteredProducts"
      @toggle-profile-menu="toggleProfileMenu"
      @open-balance="openBalanceModal"
      @open-orders="openOrdersModal"
      @logout="logout"
      @select-category="selectedCategory = $event"
    />

    <Modals
      :showBalanceModal="showBalanceModal"
      :showOrdersModal="showOrdersModal"
      :balance="userBalance"
      :wallet="user?.wallet ?? 0"
      :correctionPoints="user?.correction_points ?? 0"
      :coalitionScore="user?.coalition_score ?? 0"
      :threshold="user?.threshold ?? 0"
      :orders="orders"
      @close="closeModals"
    />
  </div>
</template>

<script>
import LoginPage from './pages/LoginPage.vue'
import LoadingPage from './pages/LoadingPage.vue'
import ShopPage from './pages/ShopPage.vue'
import Modals from './components/Modals.vue'
import { loginWith42, loginWithLearningHub, fetchMe } from './services/api'

export default {
  components: {
    LoginPage,
    LoadingPage,
    ShopPage,
    Modals
  },
  data() {
    return {
      page: 'login',
      user: null,
      showProfileMenu: false,
      showBalanceModal: false,
      showOrdersModal: false,
      selectedCategory: 'Featured',
      categories: [
        'Featured',
        'Electronics',
        'Gaming',
        'Clothes',
        'Accessories',
        'Collectibles'
      ],
      products: [
        { id: 1, category: 'Featured', name: 'Neon Keyboard', description: 'RGB mechanical keyboard.', price: 120, emoji: '⌨️' },
        { id: 2, category: 'Electronics', name: 'Smart Headphones', description: 'Noise cancelling headset.', price: 240, emoji: '🎧' },
        { id: 3, category: 'Gaming', name: 'Pro Controller', description: 'Competitive wireless controller.', price: 180, emoji: '🎮' },
        { id: 4, category: 'Clothes', name: 'Hackathon Hoodie', description: 'Soft premium hoodie.', price: 90, emoji: '🧥' },
        { id: 5, category: 'Accessories', name: 'Cyber Backpack', description: 'Lightweight urban backpack.', price: 160, emoji: '🎒' },
        { id: 6, category: 'Collectibles', name: 'Limited Badge', description: 'Exclusive community collectible.', price: 300, emoji: '🏅' },
        { id: 7, category: 'Featured', name: 'Desk Lamp', description: 'Minimal ambient desk light.', price: 75, emoji: '💡' },
        { id: 8, category: 'Gaming', name: 'Gaming Mouse', description: 'Ultra-light precision mouse.', price: 110, emoji: '🖱️' }
      ],
      orders: [
        {
          id: 1001,
          date: '2026-03-28',
          total: 210,
          items: ['Neon Keyboard', 'Desk Lamp']
        },
        {
          id: 1002,
          date: '2026-03-27',
          total: 180,
          items: ['Pro Controller']
        }
      ]
    }
  },
  computed: {
    userBalance() {
      return this.user?.balance_marvins ?? 0
    },
    filteredProducts() {
      if (this.selectedCategory === 'Featured') {
        return this.products.filter(
          p =>
            p.category === 'Featured' ||
            p.category === 'Electronics' ||
            p.category === 'Gaming'
        )
      }
      return this.products.filter(p => p.category === this.selectedCategory)
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
    handleLogin42() {
      loginWith42()
    },
    handleLoginLearningHub() {
      loginWithLearningHub()
    },
    async loadProfile() {
      const token = localStorage.getItem('token')
      if (!token) {
        this.page = 'login'
        return
      }

      this.page = 'loading'

      try {
        const user = await fetchMe(token)
        this.user = {
          ...user,
          balance_marvins: user.balance_marvins ?? 0,
          wallet: user.wallet ?? 0,
          correction_points: user.correction_points ?? 0,
          coalition_score: user.coalition_score ?? 0,
          threshold: user.threshold ?? 0
        }
        this.page = 'shop'
      } catch (error) {
        localStorage.removeItem('token')
        this.user = null
        this.page = 'login'
      }
    },
    logout() {
      localStorage.removeItem('token')
      this.user = null
      this.showProfileMenu = false
      this.page = 'login'
    },
    toggleProfileMenu() {
      this.showProfileMenu = !this.showProfileMenu
    },
    openBalanceModal() {
      this.showProfileMenu = false
      this.showBalanceModal = true
    },
    openOrdersModal() {
      this.showProfileMenu = false
      this.showOrdersModal = true
    },
    closeModals() {
      this.showBalanceModal = false
      this.showOrdersModal = false
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
}

.blob {
  position: absolute;
  border-radius: 9999px;
  filter: blur(80px);
  opacity: 0.35;
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

@keyframes blobMove {
  0% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -20px) scale(1.08);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.95);
  }
  100% {
    transform: translate(0, 0) scale(1);
  }
}
</style>