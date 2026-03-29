<template>
  <header class="topbar">
    <div class="logo-container">
      <div class="topbar-title artistic">
        <span class="gradient-text">Market</span><span class="white-text">place</span>
      </div>
      <div class="title-underline"></div>
    </div>

    <div class="profile-area">
      <button class="profile-button" @click="$emit('toggle-profile-menu')">
        <div class="profile-meta">
          <div class="profile-name">{{ user?.display_name || user?.login }}</div>
          <div class="profile-balance">
            <div class="coin-mini-wrapper"><div class="coin-mini">M</div></div>
            {{ balance }}
          </div>
        </div>
        <img v-if="user && user.image_url" :src="user.image_url" alt="avatar" class="top-avatar" />
        <img v-else :src="logo42" alt="42 logo" class="top-avatar" />
      </button>

      <div v-if="showProfileMenu" class="profile-menu">
        <button class="menu-item" @click="$emit('open-balance')">Check Balance</button>
        <button class="menu-item" @click="$emit('open-orders')">Order History</button>
        <button class="menu-item danger" @click="$emit('logout')">Logout</button>
      </div>
    </div>
  </header>
</template>

<script>
import logo42 from '../assets/42.png'
export default { props: ['user', 'balance', 'showProfileMenu'], data() { return { logo42 } } }
</script>

<style scoped>
.topbar { display: flex; align-items: center; justify-content: space-between; gap: 20px; margin-bottom: 20px; }
.logo-container { position: relative; overflow: hidden; padding-bottom: 5px; }
.topbar-title.artistic { font-size: 32px; font-weight: 900; color: white; display: flex; text-transform: uppercase; font-style: italic; }
.gradient-text { background: linear-gradient(90deg, #6366f1, #22d3ee, #6366f1); background-size: 200% auto; -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; animation: shineText 3s linear infinite; }
.title-underline { position: absolute; bottom: 0; left: 0; height: 3px; background: linear-gradient(90deg, #6366f1, #22d3ee); animation: drawLine 1.2s forwards; }
@keyframes shineText { to { background-position: 200% center; } }
@keyframes drawLine { from { width: 0; } to { width: 100%; } }

.profile-area { position: relative; }
.profile-button { display: flex; align-items: center; gap: 14px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12); color: white; padding: 8px 12px 8px 18px; border-radius: 20px; cursor: pointer; backdrop-filter: blur(12px); }
.top-avatar { width: 44px; height: 44px; border-radius: 50%; object-fit: cover; }
.profile-meta { text-align: right; }
.profile-balance { display: flex; align-items: center; justify-content: flex-end; gap: 8px; font-weight: 700; color: #fbbf24; }
.coin-mini-wrapper { perspective: 400px; }
.coin-mini { width: 18px; height: 18px; background: linear-gradient(135deg, #fbbf24, #d97706); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 10px; color: #78350f; font-weight: 900; animation: rotateCoin 3s infinite linear; }
@keyframes rotateCoin { 0% { transform: rotateY(0deg); } 100% { transform: rotateY(360deg); } }
.profile-menu { position: absolute; top: calc(100% + 10px); right: 0; width: 220px; background: rgba(15,23,42,0.96); border-radius: 18px; padding: 8px; z-index: 20; }
.menu-item { width: 100%; background: transparent; border: none; color: white; text-align: left; padding: 12px; border-radius: 12px; cursor: pointer; }
.menu-item.danger { color: #fda4af; }
@media (max-width: 900px) { .topbar { flex-direction: column-reverse; } .profile-meta { text-align: left; } .profile-button { flex-direction: row-reverse; justify-content: space-between; } }
</style>