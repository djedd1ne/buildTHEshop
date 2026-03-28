<template>
  <div>
    <div v-if="showBalanceModal" class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-card">
        <h2>Your Balance</h2>
        <p class="balance-number">{{ balance }} MARVINS</p>
        <button class="close-btn" @click="$emit('close')">Close</button>
      </div>
    </div>

    <div v-if="showPictureModal" class="modal-overlay" @click.self="$emit('close')">
      <div class="modal-card">
        <h2>Modify Profile Picture</h2>
        <p class="modal-text">Paste a new image URL below.</p>
        <input
          :value="newImageUrl"
          @input="$emit('update:newImageUrl', $event.target.value)"
          type="text"
          class="url-input"
          placeholder="https://example.com/avatar.png"
        />
        <div class="modal-actions">
          <button class="close-btn" @click="$emit('close')">Cancel</button>
          <button class="save-btn" @click="$emit('save-picture')">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['showBalanceModal', 'showPictureModal', 'balance', 'newImageUrl']
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
  max-width: 420px;
  border-radius: 24px;
  padding: 24px;
  text-align: center;
  background: rgba(255,255,255,0.08);
  border: 1px solid rgba(255,255,255,0.12);
  backdrop-filter: blur(16px);
  color: white;
}

.balance-number {
  font-size: 32px;
  font-weight: 800;
  color: #67e8f9;
}

.modal-text {
  color: #cbd5e1;
}

.url-input {
  width: 100%;
  margin-top: 16px;
  padding: 14px;
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,0.12);
  background: rgba(255,255,255,0.05);
  color: white;
  outline: none;
  box-sizing: border-box;
}

.modal-actions {
  display: flex;
  gap: 12px;
  margin-top: 18px;
}

.close-btn,
.save-btn {
  flex: 1;
  padding: 14px;
  border: none;
  border-radius: 14px;
  cursor: pointer;
  font-weight: 700;
}

.close-btn {
  background: rgba(255,255,255,0.08);
  color: white;
}

.save-btn {
  background: linear-gradient(90deg, #6366f1, #22d3ee);
  color: white;
}

@media (max-width: 640px) {
  .modal-actions {
    flex-direction: column;
  }
}
</style>