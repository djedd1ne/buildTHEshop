<template>
  <div>
    <div v-if="showBalanceModal" class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-card">
        <h2>Account Balance</h2>

        <div class="balance-grid">
          <div class="balance-box primary">
            <div class="balance-label">MARVINS</div>
            <div class="balance-value">{{ balance }}</div>
          </div>

          <div class="balance-box">
            <div class="balance-label">Wallet</div>
            <div class="balance-value small">{{ wallet }}</div>
          </div>

          <div class="balance-box">
            <div class="balance-label">Evaluation Points</div>
            <div class="balance-value small">{{ correctionPoints }}</div>
          </div>

          <div class="balance-box">
            <div class="balance-label">Coalition Score</div>
            <div class="balance-value small">{{ coalitionScore }}</div>
          </div>

          <div class="balance-box">
            <div class="balance-label">Threshold</div>
            <div class="balance-value small">{{ threshold }}</div>
          </div>
        </div>

        <div class="conversion-box">
          <div class="conversion-title">Conversion Rules</div>
          <div class="conversion-line">1 evaluation point = 1 MARVIN</div>
          <div class="conversion-line">250 coalition score = 1 MARVIN</div>
          <div class="conversion-line">1 threshold = 1 MARVIN</div>
          <div class="conversion-line">100 wallet = 1 MARVIN</div>
        </div>

        <button class="close-btn" @click="$emit('close')">Close</button>
      </div>
    </div>

    <div v-if="showOrdersModal" class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-card orders-card">
        <h2>Order History</h2>

        <div v-if="orders.length === 0" class="empty-state">
          No orders yet.
        </div>

        <div v-else class="orders-list">
          <div v-for="order in orders" :key="order.id" class="order-item">
            <div class="order-top">
              <div>
                <div class="order-id">Order #{{ order.id }}</div>
                <div class="order-date">{{ order.date }}</div>
              </div>
              <div class="order-total">{{ order.total }} MARVINS</div>
            </div>

            <div class="order-products">
              <span
                v-for="item in order.items"
                :key="item"
                class="order-product-tag"
              >
                {{ item }}
              </span>
            </div>
          </div>
        </div>

        <button class="close-btn" @click="$emit('close')">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: [
    'showBalanceModal',
    'showOrdersModal',
    'balance',
    'wallet',
    'correctionPoints',
    'coalitionScore',
    'threshold',
    'orders'
  ]
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: rgba(2, 6, 23, 0.72);
  backdrop-filter: blur(8px);
}

.modal-card {
  width: 100%;
  max-width: 560px;
  border-radius: 24px;
  padding: 24px;
  text-align: center;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  backdrop-filter: blur(16px);
  color: white;
}

.orders-card {
  max-width: 650px;
  text-align: left;
}

.balance-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin: 24px 0;
}

.balance-box {
  padding: 18px;
  border-radius: 18px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
}

.balance-box.primary {
  grid-column: span 2;
}

.balance-label {
  font-size: 13px;
  color: #94a3b8;
  margin-bottom: 8px;
}

.balance-value {
  font-size: 32px;
  font-weight: 800;
  color: #67e8f9;
}

.balance-value.small {
  font-size: 24px;
}

.conversion-box {
  text-align: left;
  margin-top: 6px;
  margin-bottom: 10px;
  padding: 16px;
  border-radius: 18px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
}

.conversion-title {
  font-weight: 700;
  margin-bottom: 10px;
}

.conversion-line {
  color: #cbd5e1;
  font-size: 14px;
  margin-bottom: 6px;
}

.empty-state {
  margin: 20px 0;
  color: #cbd5e1;
}

.orders-list {
  margin: 20px 0;
  display: grid;
  gap: 14px;
}

.order-item {
  padding: 16px;
  border-radius: 18px;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
}

.order-top {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: flex-start;
}

.order-id {
  font-weight: 700;
  color: white;
}

.order-date {
  font-size: 13px;
  color: #94a3b8;
  margin-top: 4px;
}

.order-total {
  font-weight: 800;
  color: #67e8f9;
}

.order-products {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.order-product-tag {
  padding: 8px 10px;
  border-radius: 9999px;
  background: rgba(255,255,255,0.08);
  color: #e2e8f0;
  font-size: 13px;
}

.close-btn {
  width: 100%;
  margin-top: 14px;
  padding: 14px;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  font-weight: 700;
  background: linear-gradient(90deg, #6366f1, #22d3ee);
  color: white;
}

@media (max-width: 640px) {
  .balance-grid {
    grid-template-columns: 1fr;
  }

  .balance-box.primary {
    grid-column: span 1;
  }

  .order-top {
    flex-direction: column;
  }
}
</style>