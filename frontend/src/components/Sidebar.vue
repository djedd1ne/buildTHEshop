<template>
  <aside class="sidebar">
    <h2 class="sidebar-title">Categories</h2>
    <button
      v-for="category in categories"
      :key="category"
      class="category-item"
      :class="{ active: selectedCategory === category }"
      @click="$emit('select-category', category)"
    >
      {{ category }}
    </button>
  </aside>
</template>

<script>
export default {
  props: ['categories', 'selectedCategory']
}
</script>

<style scoped>
.sidebar {
  border-radius: 24px;
  padding: 20px;
  height: fit-content;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  backdrop-filter: blur(16px);
  box-shadow: 0 20px 60px rgba(0,0,0,0.25);
}

.sidebar-title {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 18px;
  color: white;
}

.category-item {
  width: 100%;
  text-align: left;
  padding: 12px 14px;
  margin-bottom: 10px;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  background: rgba(255,255,255,0.04);
  color: white;
}

.category-item.active,
.category-item:hover {
  background: linear-gradient(90deg, #6366f1, #22d3ee);
}
</style>