<template>
  <div class="login-page-root">
    <canvas ref="particleCanvas" class="network-canvas"></canvas>

    <div class="centered">
      <LoginCard
        @login-42="$emit('login-42')"
        @login-learninghub="$emit('login-learninghub')"
      />
    </div>
  </div>
</template>

<script>
import LoginCard from '../components/LoginCard.vue'

export default {
  components: {
    LoginCard
  },
  data() {
    return {
      canvas: null,
      ctx: null,
      particles: [],
      properties: {
        count: 120,          // How many dots
        color: '#22d3ee',    // Cyan glow color
        radius: 2,           // Particle size
        speed: 0.6,          // Movement speed
        lineDist: 160,       // Max distance to draw a line
        opacity: 0.1         // Max line opacity
      },
      mouse: { x: null, y: null },
      animationId: null
    }
  },
  mounted() {
    // Initial setup
    this.canvas = this.$refs.particleCanvas;
    this.ctx = this.canvas.getContext('2d');
    this.resizeCanvas();
    this.initParticles();

    // Event listeners
    window.addEventListener('resize', this.handleResize);
    window.addEventListener('mousemove', this.handleMouseMove);
    
    // Start animation loop
    this.animate();
  },
  beforeUnmount() {
    // Clean up to prevent memory leaks
    window.removeEventListener('resize', this.handleResize);
    window.removeEventListener('mousemove', this.handleMouseMove);
    cancelAnimationFrame(this.animationId);
  },
  methods: {
    resizeCanvas() {
      this.canvas.width = window.innerWidth;
      this.canvas.height = window.innerHeight;
    },
    handleResize() {
      this.resizeCanvas();
      this.initParticles(); // Re-init on resize for best distribution
    },
    handleMouseMove(e) {
      this.mouse.x = e.clientX;
      this.mouse.y = e.clientY;
    },
    initParticles() {
      this.particles = [];
      for (let i = 0; i < this.properties.count; i++) {
        this.particles.push({
          x: Math.random() * this.canvas.width,
          y: Math.random() * this.canvas.height,
          vx: (Math.random() - 0.5) * this.properties.speed,
          vy: (Math.random() - 0.5) * this.properties.speed
        });
      }
    },
    animate() {
      // Clear canvas with deep gradient background
      const gradient = this.ctx.createRadialGradient(
        this.canvas.width / 2, this.canvas.height / 2, 0,
        this.canvas.width / 2, this.canvas.height / 2, this.canvas.width / 1.3
      );
      gradient.addColorStop(0, '#0f172a'); // Slightly lighter blue center
      gradient.addColorStop(1, '#020617'); // Dark edges
      this.ctx.fillStyle = gradient;
      this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

      this.ctx.fillStyle = this.properties.color;
      this.ctx.lineWidth = 0.6; // Thin connection lines
      this.ctx.strokeStyle = this.properties.color;

      // Draw and update particles
      for (let i = 0; i < this.particles.length; i++) {
        let p = this.particles[i];

        // Move particles
        p.x += p.vx;
        p.y += p.vy;

        // Bounce off walls
        if (p.x < 0 || p.x > this.canvas.width) p.vx *= -1;
        if (p.y < 0 || p.y > this.canvas.height) p.vy *= -1;

        // Draw particle dot
        this.ctx.beginPath();
        this.ctx.arc(p.x, p.y, this.properties.radius, 0, Math.PI * 2);
        this.ctx.fill();

        // Check distance with mouse to attract lines (interactive effect)
        const dxMouse = p.x - this.mouse.x;
        const dyMouse = p.y - this.mouse.y;
        const distMouse = Math.sqrt(dxMouse * dxMouse + dyMouse * dyMouse);
        
        // Slightly pull particles toward mouse (optional magnetic effect)
        if (distMouse < 250) {
            p.vx += dxMouse * 0.00002;
            p.vy += dyMouse * 0.00002;
        }

        // Draw lines between nearby particles
        for (let j = i + 1; j < this.particles.length; j++) {
          let p2 = this.particles[j];
          const dx = p.x - p2.x;
          const dy = p.y - p2.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          // Draw line if close enough
          if (dist < this.properties.lineDist) {
            // Dynamic opacity based on distance (closer = brighter)
            const opacity = 1 - dist / this.properties.lineDist;
            this.ctx.globalAlpha = opacity * this.properties.opacity;
            
            this.ctx.beginPath();
            this.ctx.moveTo(p.x, p.y);
            this.ctx.lineTo(p2.x, p2.y);
            this.ctx.stroke();
          }
        }
        this.ctx.globalAlpha = 1; // Reset alpha
      }

      this.animationId = requestAnimationFrame(this.animate);
    }
  }
}
</script>

<style scoped>
.login-page-root {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  /* Deep space background fallback */
  background: linear-gradient(180deg, #020617 0%, #0f172a 100%);
}

.network-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 1; /* Below the card, above the base background */
}

.centered {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  z-index: 10; /* Put the login card high above the particle canvas */
}
</style>