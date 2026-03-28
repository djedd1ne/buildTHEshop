<template>
  <header class="topbar">
    <div class="profile-area">
      <button class="profile-button" @click="$emit('toggle-profile-menu')">
        <img
          v-if="user && user.image_url"
          :src="user.image_url"
          alt="avatar"
          class="top-avatar"
        />
        <img
          v-else
          :src="logo42"
          alt="42 logo"
          class="top-avatar"
        />
        <div class="profile-meta">
          <div class="profile-name">{{ user?.display_name || user?.login }}</div>
          <div class="profile-balance">{{ balance }} MARVINS</div>
        </div>
      </button>

      <div v-if="showProfileMenu" class="profile-menu">
        <button class="menu-item" @click="$emit('open-balance')">Check Balance</button>
        <button class="menu-item" @click="$emit('open-orders')">Order History</button>
        <button class="menu-item danger" @click="$emit('logout')">Logout</button>
      </div>
    </div>

    <div class="topbar-title">Marketplace</div>
  </header>
</template>

<script>
import logo42 from '../assets/42.png'

export default {
  props: ['user', 'balance', 'showProfileMenu'],
  data() {
    return {
      logo42
    }
  }
}
</script>

<style scoped>
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 20px;
}

.profile-area {
  position: relative;
}

.profile-button {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  color: white;
  padding: 10px 14px;
  border-radius: 18px;
  cursor: pointer;
  backdrop-filter: blur(12px);
}

.top-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-name {
  font-weight: 700;
}

.profile-balance {
  font-size: 13px;
  color: #cbd5e1;
}

.profile-menu {
  position: absolute;
  top: calc(100% + 10px);
  left: 0;
  width: 220px;
  background: rgba(15,23,42,0.96);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 18px;
  padding: 8px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.35);
  z-index: 20;
}

.menu-item {
  width: 100%;
  background: transparent;
  border: none;
  color: white;
  text-align: left;
  padding: 12px;
  border-radius: 12px;
  cursor: pointer;
}

.menu-item:hover {
  background: rgba(255,255,255,0.08);
}

.menu-item.danger {
  color: #fda4af;
}

.topbar-title {
  font-size: 28px;
  font-weight: 800;
  color: white;
}

@media (max-width: 900px) {
  .topbar {
    flex-direction: column;
    align-items: stretch;
  }

  .topbar-title {
    font-size: 24px;
  }
}

@media (max-width: 640px) {
  .profile-button {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>