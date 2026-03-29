<template>
  <div class="page" @click="handleGlobalClick">
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
      @buy-product="openPurchaseConfirm"
    />

    <Modals
      :showBalanceModal="showBalanceModal"
      :showOrdersModal="showOrdersModal"
      :showPurchaseConfirm="showPurchaseConfirm"
      :showPurchaseResult="showPurchaseResult"
      :purchaseProduct="purchaseTarget"
      :purchaseResultSuccess="purchaseResultSuccess"
      :purchaseResultMessage="purchaseResultMessage"
      :purchaseLoading="purchaseLoading"
      :balance="userBalance"
      :wallet="user?.wallet ?? 0"
      :correctionPoints="user?.correction_points ?? 0"
      :coalitionScore="user?.coalition_score ?? 0"
      :threshold="user?.threshold ?? 0"
      :orders="orders"
      :ordersLoading="ordersLoading"
      @close="closeModals"
      @confirm-purchase="confirmPurchase"
      @close-result="closePurchaseResult"
    />
  </div>
</template>

<script>
import LoginPage from './pages/LoginPage.vue'
import LoadingPage from './pages/LoadingPage.vue'
import ShopPage from './pages/ShopPage.vue'
import Modals from './components/Modals.vue'
import { loginWith42, loginWithLearningHub, fetchMe, purchaseProduct, fetchOrders } from './services/api'

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
      showPurchaseConfirm: false,
      showPurchaseResult: false,
      purchaseTarget: null,
      purchaseResultSuccess: false,
      purchaseResultMessage: '',
      purchaseLoading: false,
      ordersLoading: false,
      selectedCategory: 'Featured',
      categories: [
        'Featured',
        'Academic',
        'Campus Privileges',
        'Fun & Social'
      ],
      products: [
        // ── Academic ──
        {
          id: 1,
          category: 'Academic',
          name: 'Eval Fast Pass',
          description: 'Skip the evaluation queue, get matched with an evaluator instantly.',
          price: 30,
          emoji: '⚡'
        },
        {
          id: 2,
          category: 'Academic',
          name: 'Senior Mentoring Session',
          description: 'Book a 1-hour session with a Level 10+ student on any project.',
          price: 40,
          emoji: '🧑‍🏫'
        },
        {
          id: 3,
          category: 'Academic',
          name: 'Blackhole Lifeline',
          description: 'Extend your blackhole deadline by 48 hours.',
          price: 50,
          emoji: '🕳️'
        },
        {
          id: 4,
          category: 'Academic',
          name: 'Dream Team Matchmaker',
          description: 'Get paired with a high-level student for your next group project.',
          price: 35,
          emoji: '🤝'
        },

        // ── Campus Privileges ──
        {
          id: 5,
          category: 'Campus Privileges',
          name: 'Reserved Seat',
          description: 'Claim your favorite desk for a full day.',
          price: 10,
          emoji: '🪑'
        },
        {
          id: 6,
          category: 'Campus Privileges',
          name: 'Reserved Seat Pro',
          description: 'Claim your favorite desk for an entire week.',
          price: 35,
          emoji: '💺⭐'
        },
        {
          id: 7,
          category: 'Campus Privileges',
          name: 'Dual Monitor Pass',
          description: 'Reserve a dual-monitor workstation for a day.',
          price: 20,
          emoji: '🖥️🖥️'
        },
        {
          id: 8,
          category: 'Campus Privileges',
          name: 'VIP Wi-Fi',
          description: 'Access to a faster dedicated Wi-Fi network for a day.',
          price: 15,
          emoji: '📶'
        },
        {
          id: 9,
          category: 'Campus Privileges',
          name: 'Whiteboard Reservation',
          description: 'Reserve a personal whiteboard for a day.',
          price: 8,
          emoji: '📋✏️'
        },

        // ── Fun & Social ──
        {
          id: 10,
          category: 'Fun & Social',
          name: 'Meme of the Day',
          description: 'Your meme gets featured on all campus screens for a full day.',
          price: 25,
          emoji: '📸'
        },
        {
          id: 11,
          category: 'Fun & Social',
          name: 'Event VIP Access',
          description: 'Priority sign-up for the next campus workshop or event.',
          price: 30,
          emoji: '🎟️'
        },
        {
          id: 12,
          category: 'Fun & Social',
          name: 'Desk Plant Buddy',
          description: 'A small plant placed at your desk for a week.',
          price: 12,
          emoji: '🌿'
        },
        {
          id: 13,
          category: 'Fun & Social',
          name: '"Legend" Title',
          description: 'A special "Legend" badge next to your name on campus boards.',
          price: 45,
          emoji: '👑'
        },
        {
          id: 14,
          category: 'Fun & Social',
          name: 'Ping Pong Priority',
          description: 'Skip the queue for the ping pong table all day.',
          price: 5,
          emoji: '🏓'
        }
      ],
      orders: []
    }
  },
  computed: {
    userBalance() {
      return this.user?.balance_marvins ?? 0
    },
    filteredProducts() {
      if (this.selectedCategory === 'Featured') {
        const featuredIds = [3, 1, 13, 7, 10, 14]
        return this.products.filter(p => featuredIds.includes(p.id))
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
    handleGlobalClick(e) {
      if (this.showProfileMenu && !e.target.closest('.profile-area')) {
        this.showProfileMenu = false
      }
    },
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
    async openOrdersModal() {
      this.showProfileMenu = false
      this.showOrdersModal = true
      this.ordersLoading = true

      try {
        const token = localStorage.getItem('token')
        if (token) {
          this.orders = await fetchOrders(token)
        }
      } catch (err) {
        console.error('Failed to load orders:', err)
        this.orders = []
      } finally {
        this.ordersLoading = false
      }
    },
    openPurchaseConfirm(product) {
      this.purchaseTarget = product
      this.showPurchaseConfirm = true
    },
    async confirmPurchase() {
      if (!this.purchaseTarget) return

      this.purchaseLoading = true

      try {
        const token = localStorage.getItem('token')
        const result = await purchaseProduct(token, this.purchaseTarget)

        this.user = {
          ...this.user,
          balance_marvins: result.new_balance
        }

        this.showPurchaseConfirm = false
        this.purchaseResultSuccess = true
        this.purchaseResultMessage = `You bought ${this.purchaseTarget.name} for ${this.purchaseTarget.price} MARVINS!`
        this.showPurchaseResult = true
      } catch (err) {
        this.showPurchaseConfirm = false
        this.purchaseResultSuccess = false
        this.purchaseResultMessage = err.message || 'Purchase failed'
        this.showPurchaseResult = true
      } finally {
        this.purchaseLoading = false
      }
    },
    closePurchaseResult() {
      this.showPurchaseResult = false
      this.purchaseTarget = null
      this.purchaseResultMessage = ''
    },
    closeModals() {
      this.showBalanceModal = false
      this.showOrdersModal = false
      this.showPurchaseConfirm = false
      this.showPurchaseResult = false
      this.purchaseTarget = null
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