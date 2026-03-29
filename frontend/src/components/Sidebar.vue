<template>
  <aside class="sidebar">
    <h2 class="sidebar-title">🗂️ Categories</h2>
    <button
      v-for="category in categories"
      :key="category"
      class="category-item"
      :class="{ active: selectedCategory === category }"
      @click="$emit('select-category', category)"
    >
      <span class="cat-icon">{{ catIcon(category) }}</span>
      <span class="cat-label">{{ category }}</span>
      <span v-if="selectedCategory === category" class="active-dot"></span>
    </button>
  </aside>
</template>

<script>
export default {
  props: ['categories', 'selectedCategory'],
  methods: {
    catIcon(cat) {
      const icons = {
        'Featured': '⭐',
        'Academic': '📚',
        'Campus Privileges': '🏫',
        'Fun & Social': '🎉'
      }
      return icons[cat] || '📁'
    }
  }
}
</script>

<style scoped>
.sidebar {
  border-radius: 24px;
  padding: 20px;
  height: fit-content;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(16px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
}

.sidebar-title {
  margin-top: 0;
  margin-bottom: 18px;
  font-size: 18px;
  color: white;
  font-weight: 800;
}

.category-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  text-align: left;
  padding: 13px 14px;
  margin-bottom: 8px;
  border: 1px solid transparent;
  border-radius: 16px;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.04);
  color: #cbd5e1;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
}

.category-item:hover {
  background: rgba(255, 255, 255, 0.08);
  color: white;
  transform: translateX(4px);
}

.category-item.active {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(34, 211, 238, 0.15));
  border-color: rgba(99, 102, 241, 0.35);
  color: white;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.15);
}

.cat-icon {
  font-size: 18px;
  transition: transform 0.3s ease;
}

.category-item:hover .cat-icon,
.category-item.active .cat-icon {
  transform: scale(1.2);
}

.cat-label {
  flex: 1;
}

.active-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #22d3ee;
  box-shadow: 0 0 8px rgba(34, 211, 238, 0.6);
  animation: dotPulse 1.5s ease-in-out infinite;
}

@keyframes dotPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(0.8); }
}
</style>