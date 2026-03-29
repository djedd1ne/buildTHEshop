<template>
  <div>
    <!-- Balance Modal -->
    <Transition name="modal">
      <div v-if="showBalanceModal" class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-card">
          <div class="modal-header">
            <h2>💰 Account Balance</h2>
          </div>

          <div class="balance-grid">
            <div class="balance-box primary">
              <div class="balance-label">MARVINS</div>
              <div class="balance-value main-balance">
                <span class="balance-coin">🪙</span>
                {{ balance }}
              </div>
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
            <div class="conversion-title">📐 Conversion Rules</div>
            <div class="conversion-line">1 evaluation point = 1 MARVIN</div>
            <div class="conversion-line">100 coalition score = 1 MARVIN</div>
            <div class="conversion-line">1 threshold = 1 MARVIN</div>
            <div class="conversion-line">100 wallet = 1 MARVIN</div>
          </div>

          <button class="close-btn" @click="$emit('close')">Close</button>
        </div>
      </div>
    </Transition>

    <!-- Orders Modal -->
    <Transition name="modal">
      <div v-if="showOrdersModal" class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-card orders-card">
          <div class="modal-header">
            <h2>📦 Order History</h2>
          </div>

          <div v-if="ordersLoading" class="loading-state">
            <div class="mini-spinner"></div>
            <p>Loading orders...</p>
          </div>

          <div v-else-if="orders.length === 0" class="empty-state">
            <div class="empty-icon">🛒</div>
            <p>No orders yet. Start shopping!</p>
          </div>

          <div v-else class="orders-list">
            <div v-for="order in orders" :key="order.id" class="order-item">
              <div class="order-top">
                <div>
                  <div class="order-id">Order #{{ order.id }}</div>
                  <div class="order-date">{{ order.date }}</div>
                </div>
                <div class="order-total">
                  <span class="order-coin">🪙</span>
                  {{ order.total }} MARVINS
                </div>
              </div>

              <div class="order-products">
                <span
                  v-for="(item, idx) in order.items"
                  :key="idx"
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
    </Transition>

    <!-- Purchase Confirmation Modal -->
    <Transition name="modal">
      <div v-if="showPurchaseConfirm" class="modal-overlay" @click.self="$emit('close')">
        <div class="modal-card purchase-card">
          <div class="purchase-emoji-wrapper">
            <div class="purchase-emoji">{{ purchaseProduct?.emoji }}</div>
          </div>
          <h2 class="purchase-title">Confirm Purchase</h2>
          <p class="purchase-product-name">{{ purchaseProduct?.name }}</p>
          <p class="purchase-product-desc">{{ purchaseProduct?.description }}</p>

          <div class="purchase-summary">
            <div class="summary-row">
              <span class="summary-label">Price</span>
              <span class="summary-value price-highlight">
                <span class="summary-coin">🪙</span>
                {{ purchaseProduct?.price }} MARVINS
              </span>
            </div>
            <div class="summary-divider"></div>
            <div class="summary-row">
              <span class="summary-label">Your Balance</span>
              <span class="summary-value">{{ balance }} MARVINS</span>
            </div>
            <div class="summary-row">
              <span class="summary-label">After Purchase</span>
              <span
                class="summary-value"
                :class="{ 'insufficient': balance - (purchaseProduct?.price || 0) < 0 }"
              >
                {{ balance - (purchaseProduct?.price || 0) }} MARVINS
              </span>
            </div>
          </div>

          <div v-if="balance < (purchaseProduct?.price || 0)" class="insufficient-warning">
            ⚠️ You don't have enough MARVINS for this purchase.
          </div>

          <div class="purchase-actions">
            <button class="cancel-btn" @click="$emit('close')" :disabled="purchaseLoading">
              Cancel
            </button>
            <button
              class="confirm-btn"
              @click="$emit('confirm-purchase')"
              :disabled="purchaseLoading || balance < (purchaseProduct?.price || 0)"
            >
              <span v-if="purchaseLoading" class="btn-spinner"></span>
              <span v-else>🛒 Confirm</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Purchase Result Modal -->
    <Transition name="modal">
      <div v-if="showPurchaseResult" class="modal-overlay" @click.self="$emit('close-result')">
        <div class="modal-card result-card">
          <div class="result-icon-wrapper">
            <div class="result-icon" :class="{ success: purchaseResultSuccess, failure: !purchaseResultSuccess }">
              {{ purchaseResultSuccess ? '✅' : '❌' }}
            </div>
          </div>
          <h2>{{ purchaseResultSuccess ? 'Purchase Complete!' : 'Purchase Failed' }}</h2>
          <p class="result-message">{{ purchaseResultMessage }}</p>
          <button class="close-btn" @click="$emit('close-result')">OK</button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script>
export default {
  props: [
    'showBalanceModal',
    'showOrdersModal',
    'showPurchaseConfirm',
    'showPurchaseResult',
    'purchaseProduct',
    'purchaseResultSuccess',
    'purchaseResultMessage',
    'purchaseLoading',
    'balance',
    'wallet',
    'correctionPoints',
    'coalitionScore',
    'threshold',
    'orders',
    'ordersLoading'
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
  background: rgba(2, 6, 23, 0.75);
  backdrop-filter: blur(10px);
}

.modal-card {
  width: 100%;
  max-width: 560px;
  border-radius: 24px;
  padding: 28px;
  text-align: center;
  background: rgba(15, 23, 42, 0.96);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(16px);
  color: white;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5),
              0 0 40px rgba(99, 102, 241, 0.08);
}

.modal-header h2 {
  margin: 0 0 4px 0;
  font-size: 24px;
  font-weight: 800;
}

.orders-card {
  max-width: 650px;
  text-align: left;
}

.orders-card .modal-header {
  text-align: center;
}

/* Balance */
.balance-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin: 24px 0;
}

.balance-box {
  padding: 18px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: background 0.2s, border-color 0.2s;
}

.balance-box:hover {
  background: rgba(255, 255, 255, 0.07);
  border-color: rgba(255, 255, 255, 0.12);
}

.balance-box.primary {
  grid-column: span 2;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(34, 211, 238, 0.15));
  border: 1px solid rgba(99, 102, 241, 0.3);
}

.balance-label {
  font-size: 12px;
  color: #94a3b8;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 0.8px;
  font-weight: 600;
}

.balance-value {
  font-size: 32px;
  font-weight: 800;
  color: #67e8f9;
}

.balance-value.small {
  font-size: 24px;
}

.main-balance {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

.balance-coin {
  font-size: 32px;
  animation: coinSpin 2s ease-in-out infinite;
}

@keyframes coinSpin {
  0% { transform: rotateY(0deg); }
  50% { transform: rotateY(180deg); }
  100% { transform: rotateY(360deg); }
}

.conversion-box {
  text-align: left;
  margin-top: 6px;
  margin-bottom: 10px;
  padding: 16px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.conversion-title {
  font-weight: 700;
  margin-bottom: 10px;
}

.conversion-line {
  color: #94a3b8;
  font-size: 14px;
  margin-bottom: 6px;
}

/* Orders */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 30px 0;
  color: #94a3b8;
}

.mini-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(255, 255, 255, 0.12);
  border-top: 3px solid #22d3ee;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 40px 0;
  color: #64748b;
  text-align: center;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 4px;
  animation: emptyBounce 2s ease-in-out infinite;
}

@keyframes emptyBounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.orders-list {
  margin: 20px 0;
  display: grid;
  gap: 14px;
  max-height: 400px;
  overflow-y: auto;
}

.order-item {
  padding: 16px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.06);
  transition: background 0.2s, transform 0.2s;
}

.order-item:hover {
  background: rgba(255, 255, 255, 0.07);
  transform: translateX(3px);
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
  color: #64748b;
  margin-top: 4px;
}

.order-total {
  font-weight: 800;
  color: #67e8f9;
  white-space: nowrap;
  display: flex;
  align-items: center;
  gap: 4px;
}

.order-coin {
  font-size: 16px;
}

.order-products {
  margin-top: 14px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.order-product-tag {
  padding: 6px 12px;
  border-radius: 9999px;
  background: rgba(99, 102, 241, 0.12);
  border: 1px solid rgba(99, 102, 241, 0.2);
  color: #c7d2fe;
  font-size: 13px;
  font-weight: 500;
}

/* Purchase Confirmation */
.purchase-card {
  max-width: 480px;
}

.purchase-emoji-wrapper {
  margin-bottom: 8px;
}

.purchase-emoji {
  font-size: 60px;
  animation: purchaseFloat 2s ease-in-out infinite;
}

@keyframes purchaseFloat {
  0%, 100% { transform: translateY(0) scale(1); }
  50% { transform: translateY(-8px) scale(1.05); }
}

.purchase-title {
  margin: 0;
  font-size: 24px;
  font-weight: 800;
}

.purchase-product-name {
  font-size: 18px;
  font-weight: 700;
  color: #e2e8f0;
  margin: 8px 0 4px;
}

.purchase-product-desc {
  color: #94a3b8;
  font-size: 14px;
  margin-bottom: 20px;
}

.purchase-summary {
  padding: 18px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  margin-bottom: 16px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
}

.summary-label {
  color: #94a3b8;
  font-size: 14px;
}

.summary-value {
  font-weight: 700;
  font-size: 15px;
}

.price-highlight {
  color: #67e8f9;
  font-size: 18px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.summary-coin {
  font-size: 18px;
  animation: coinSpin 1.5s ease-in-out infinite;
}

.summary-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.06);
  margin: 8px 0;
}

.insufficient {
  color: #fda4af;
}

.insufficient-warning {
  padding: 12px;
  border-radius: 14px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #fda4af;
  font-size: 14px;
  margin-bottom: 16px;
}

.purchase-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.cancel-btn {
  padding: 14px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 14px;
  cursor: pointer;
  font-weight: 700;
  font-size: 15px;
  background: rgba(255, 255, 255, 0.05);
  color: #cbd5e1;
  transition: all 0.2s;
}

.cancel-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: white;
}

.confirm-btn {
  padding: 14px;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  font-weight: 700;
  font-size: 15px;
  background: linear-gradient(135deg, #6366f1, #22d3ee);
  color: white;
  transition: all 0.25s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.confirm-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
}

.confirm-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.btn-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

/* Result */
.result-card {
  max-width: 420px;
}

.result-icon-wrapper {
  margin-bottom: 8px;
}

.result-icon {
  font-size: 60px;
  display: inline-block;
}

.result-icon.success {
  animation: successPop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.result-icon.failure {
  animation: failShake 0.5s ease;
}

@keyframes successPop {
  0% { transform: scale(0); }
  50% { transform: scale(1.3); }
  100% { transform: scale(1); }
}

@keyframes failShake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-8px); }
  50% { transform: translateX(8px); }
  75% { transform: translateX(-4px); }
}

.result-message {
  color: #94a3b8;
  margin: 12px 0 20px;
  font-size: 15px;
  line-height: 1.5;
}

/* Close Button */
.close-btn {
  width: 100%;
  margin-top: 14px;
  padding: 14px;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  font-weight: 700;
  font-size: 15px;
  background: linear-gradient(135deg, #6366f1, #22d3ee);
  color: white;
  transition: transform 0.2s, box-shadow 0.2s;
}

.close-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
}

/* Transitions */
.modal-enter-active {
  transition: opacity 0.25s ease;
}
.modal-enter-active .modal-card {
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.25s ease;
}
.modal-leave-active {
  transition: opacity 0.2s ease;
}
.modal-leave-active .modal-card {
  transition: transform 0.2s ease, opacity 0.2s ease;
}
.modal-enter-from {
  opacity: 0;
}
.modal-enter-from .modal-card {
  transform: scale(0.88) translateY(10px);
  opacity: 0;
}
.modal-leave-to {
  opacity: 0;
}
.modal-leave-to .modal-card {
  transform: scale(0.92);
  opacity: 0;
}

@keyframes spin {
  to { transform: rotate(360deg); }
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

  .purchase-actions {
    grid-template-columns: 1fr;
  }
}
</style>