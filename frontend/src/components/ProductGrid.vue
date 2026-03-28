<template>
  <main class="market-section">
    <div class="market-header">
      <h2>{{ selectedCategory }}</h2>
      <p>Browse items and spend your MARVINS wisely.</p>
    </div>

    <div class="product-grid">
      <div
        v-for="product in products"
        :key="product.id"
        class="product-card"
      >
        <div class="product-image">{{ product.emoji }}</div>
        <div class="product-name">{{ product.name }}</div>
        <div class="product-desc">{{ product.description }}</div>
        <div class="product-footer">
          <span class="price">{{ product.price }} MARVINS</span>
          <button class="buy-btn">Buy</button>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
export default {
  props: ['products', 'selectedCategory']
}
</script>

<style scoped>
.market-section {
  border-radius: 24px;
  padding: 24px;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  backdrop-filter: blur(16px);
  box-shadow: 0 20px 60px rgba(0,0,0,0.25);
  color: white;
}

.market-header h2 {
  margin: 0;
  font-size: 28px;
}

.market-header p {
  margin-top: 6px;
  color: #cbd5e1;
}

.product-grid {
  margin-top: 24px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 18px;
}

.product-card {
  border-radius: 22px;
  padding: 20px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  transition: transform 0.25s ease, background 0.25s ease;
}

.product-card:hover {
  transform: translateY(-4px);
  background: rgba(255,255,255,0.08);
}

.product-image {
  font-size: 40px;
}

.product-name {
  margin-top: 16px;
  font-weight: 700;
  font-size: 18px;
}

.product-desc {
  margin-top: 8px;
  color: #cbd5e1;
  font-size: 14px;
}

.product-footer {
  margin-top: 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.price {
  font-weight: 800;
  color: #67e8f9;
}

.buy-btn {
  padding: 10px 14px;
  border: none;
  border-radius: 14px;
  background: linear-gradient(90deg, #6366f1, #22d3ee);
  color: white;
  cursor: pointer;
}

@media (max-width: 640px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
}
</style>