<template>
  <div class="centered">
    <LoginCard @login="$emit('login')" />
  </div>
</template>

<script>
import LoginCard from '../components/LoginCard.vue'

export default {
  components: {
    LoginCard
  }
}
</script>

<style scoped>
.centered {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  z-index: 2;
}
</style>