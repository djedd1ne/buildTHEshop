<template>
  <div class="page">
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    <div class="blob blob-3"></div>

    <LoginPage
      v-if="page === 'login'"
      @login="handleLogin"
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
      @open-picture="openPictureModal"
      @logout="logout"
      @select-category="selectedCategory = $event"
    />

    <Modals
      :showBalanceModal="showBalanceModal"
      :showPictureModal="showPictureModal"
      :balance="userBalance"
      :newImageUrl="newImageUrl"
      @close="closeModals"
      @update:newImageUrl="newImageUrl = $event"
      @save-picture="updateProfilePicture"
    />
  </div>
</template>

<script>
import LoginPage from './pages/LoginPage.vue'
import LoadingPage from './pages/LoadingPage.vue'
import ShopPage from './pages/ShopPage.vue'
import Modals from './components/Modals.vue'
import { loginWith42, fetchMe } from './services/api'

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
      showPictureModal: false,
      newImageUrl: '',
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
      ]
    }
  },
  computed: {
    userBalance() {
      return this.user?.balance_marvins ?? 1337
    },
    filteredProducts() {
      if (this.selectedCategory === 'Featured') {
        return this.products.filter(
          p => p.category === 'Featured' || p.category === 'Electronics' || p.category === 'Gaming'
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
    handleLogin() {
      loginWith42()
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
          balance_marvins: user.balance_marvins ?? 1337
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
    openPictureModal() {
      this.showProfileMenu = false
      this.newImageUrl = this.user?.image_url || ''
      this.showPictureModal = true
    },
    closeModals() {
      this.showBalanceModal = false
      this.showPictureModal = false
    },
    updateProfilePicture() {
      if (this.newImageUrl && this.user) {
        this.user.image_url = this.newImageUrl
      }
      this.closeModals()
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
  0% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -20px) scale(1.08); }
  66% { transform: translate(-20px, 20px) scale(0.95); }
  100% { transform: translate(0, 0) scale(1); }
}
</style>