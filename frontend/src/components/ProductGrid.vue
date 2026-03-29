<template>
  <main class="market-section">
    <div class="market-header">
      <h2>
        <span class="header-icon">{{ categoryIcon }}</span>
        {{ selectedCategory }}
      </h2>
      <p>Browse perks and spend your MARVINS wisely.</p>
    </div>

    <div class="product-grid">
      <div
        v-for="product in products"
        :key="product.id"
        class="product-card"
        @mouseenter="hoveredId = product.id"
        @mouseleave="hoveredId = null"
        @touchstart="hoveredId = product.id"
        @touchend="hoveredId = null"
      >
        <!-- Glow effect on hover -->
        <div class="card-glow" :class="{ active: hoveredId === product.id }"></div>

        <!-- Animated emoji -->
        <div class="product-emoji-wrapper">
          <div
            class="product-emoji"
            :class="{ bouncing: hoveredId === product.id }"
          >
            {{ product.emoji }}
          </div>
          <div
            class="emoji-shadow"
            :class="{ active: hoveredId === product.id }"
          ></div>
        </div>

        <!-- Info -->
        <div class="product-name">{{ product.name }}</div>
        <div class="product-desc">{{ product.description }}</div>

        <!-- Category tag -->
        <div class="product-tag" :class="tagClass(product.category)">
          {{ product.category }}
        </div>

        <!-- Footer -->
        <div class="product-footer">
          <div class="price-wrapper">
            <span class="coin" :class="{ spinning: hoveredId === product.id }">🪙</span>
            <span class="price">{{ product.price }}</span>
            <span class="price-label">MARVINS</span>
          </div>
          <button
            class="buy-btn"
            :class="{ pulse: hoveredId === product.id }"
            @click="$emit('buy-product', product)"
          >
            <span class="buy-icon">🛒</span>
            Buy
          </button>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
export default {
  props: ['products', 'selectedCategory'],
  emits: ['buy-product'],
  data() {
    return {
      hoveredId: null
    }
  },
  computed: {
    categoryIcon() {
      const icons = {
        'Featured': '⭐',
        'Academic': '📚',
        'Campus Privileges': '🏫',
        'Fun & Social': '🎉'
      }
      return icons[this.selectedCategory] || '🛍️'
    }
  },
  methods: {
    tagClass(category) {
      const map = {
        'Academic': 'tag-academic',
        'Campus Privileges': 'tag-campus',
        'Fun & Social': 'tag-fun'
      }
      return map[category] || 'tag-default'
    }
  }
}
</script>

<style scoped>
.market-section {
  border-radius: 24px;
  padding: 28px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(16px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
  color: white;
}

.market-header h2 {
  margin: 0;
  font-size: 28px;
  font-weight: 800;
  display: flex;
  align-items: center;
  gap: 10px;
}

.header-icon {
  font-size: 30px;
  animation: headerPulse 2s ease-in-out infinite;
}

@keyframes headerPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.15); }
}

.market-header p {
  margin-top: 6px;
  color: #94a3b8;
  font-size: 15px;
}

/* Grid */
.product-grid {
  margin-top: 24px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}

/* Card */
.product-card {
  position: relative;
  border-radius: 22px;
  padding: 22px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1),
              background 0.3s ease,
              border-color 0.3s ease,
              box-shadow 0.3s ease;
  overflow: hidden;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-8px) scale(1.02);
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(99, 102, 241, 0.35);
  box-shadow: 0 20px 50px rgba(99, 102, 241, 0.15),
              0 0 30px rgba(34, 211, 238, 0.08);
}

/* Glow */
.card-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(
    circle at center,
    rgba(99, 102, 241, 0.12) 0%,
    transparent 60%
  );
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.card-glow.active {
  opacity: 1;
}

/* Emoji */
.product-emoji-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 6px;
}

.product-emoji {
  font-size: 48px;
  transition: transform 0.3s ease;
  will-change: transform;
}

.product-emoji.bouncing {
  animation: emojiFloat 1s ease-in-out infinite;
}

@keyframes emojiFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.emoji-shadow {
  width: 40px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.06);
  margin-top: 4px;
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.emoji-shadow.active {
  transform: scaleX(0.7);
  opacity: 0.5;
}

/* Info */
.product-name {
  margin-top: 12px;
  font-weight: 700;
  font-size: 17px;
  line-height: 1.3;
}

.product-desc {
  margin-top: 6px;
  color: #94a3b8;
  font-size: 13px;
  line-height: 1.5;
}

/* Tag */
.product-tag {
  display: inline-block;
  margin-top: 12px;
  padding: 4px 10px;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tag-academic {
  background: rgba(99, 102, 241, 0.15);
  color: #a5b4fc;
  border: 1px solid rgba(99, 102, 241, 0.25);
}

.tag-campus {
  background: rgba(34, 211, 238, 0.12);
  color: #67e8f9;
  border: 1px solid rgba(34, 211, 238, 0.25);
}

.tag-fun {
  background: rgba(251, 191, 36, 0.12);
  color: #fcd34d;
  border: 1px solid rgba(251, 191, 36, 0.25);
}

.tag-default {
  background: rgba(255, 255, 255, 0.08);
  color: #cbd5e1;
  border: 1px solid rgba(255, 255, 255, 0.12);
}

/* Footer */
.product-footer {
  margin-top: 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.price-wrapper {
  display: flex;
  align-items: center;
  gap: 6px;
}

.coin {
  font-size: 20px;
  display: inline-block;
  transition: transform 0.3s ease;
}

.coin.spinning {
  animation: coinSpin 0.8s ease-in-out infinite;
}

@keyframes coinSpin {
  0% { transform: rotateY(0deg); }
  50% { transform: rotateY(180deg); }
  100% { transform: rotateY(360deg); }
}

.price {
  font-weight: 800;
  font-size: 20px;
  color: #67e8f9;
}

.price-label {
  font-size: 11px;
  color: #64748b;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 2px;
}

/* Buy Button */
.buy-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  border: none;
  border-radius: 14px;
  background: linear-gradient(135deg, #6366f1, #22d3ee);
  color: white;
  cursor: pointer;
  font-weight: 700;
  font-size: 14px;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
  white-space: nowrap;
}

.buy-btn:hover {
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 10px 25px rgba(34, 211, 238, 0.3);
}

.buy-btn.pulse {
  animation: btnPulse 1.5s ease-in-out infinite;
}

@keyframes btnPulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }
  50% { box-shadow: 0 0 0 10px rgba(99, 102, 241, 0); }
}

.buy-icon {
  font-size: 16px;
}

/* Responsive */
@media (max-width: 640px) {
  .product-grid {
    grid-template-columns: 1fr;
  }

  .product-card:hover {
    transform: translateY(-4px) scale(1.01);
  }
}
</style>