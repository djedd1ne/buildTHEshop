<template>
  <div class="shop-layout">
    <TopBar
      :user="user"
      :balance="balance"
      :showProfileMenu="showProfileMenu"
      @toggle-profile-menu="$emit('toggle-profile-menu')"
      @open-balance="$emit('open-balance')"
      @open-orders="$emit('open-orders')"
      @logout="$emit('logout')"
    />

    <div class="shop-content">
      <Sidebar
        :categories="categories"
        :selectedCategory="selectedCategory"
        @select-category="$emit('select-category', $event)"
      />

      <ProductGrid
        :products="products"
        :selectedCategory="selectedCategory"
      />
    </div>
  </div>
</template>

<script>
import TopBar from '../components/TopBar.vue'
import Sidebar from '../components/Sidebar.vue'
import ProductGrid from '../components/ProductGrid.vue'

export default {
  components: {
    TopBar,
    Sidebar,
    ProductGrid
  },
  props: [
    'user',
    'balance',
    'showProfileMenu',
    'categories',
    'selectedCategory',
    'products'
  ]
}
</script>

<style scoped>
.shop-layout {
  position: relative;
  z-index: 2;
  min-height: 100vh;
  padding: 20px;
}

.shop-content {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 20px;
}

@media (max-width: 900px) {
  .shop-content {
    grid-template-columns: 1fr;
  }
}
</style>