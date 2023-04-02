<template>
  <section class="dark-theme">
    <p class="text-color">This website was constructed with FastAPI and Vue, the perfect blend of speed and performance.</p>

    <div v-if="isLoggedIn" id="logout">
      <p id="logout" class="text-color">Click <a href="/dashboard" class="accent-color">here</a> to access all your notes and stay organized.</p>
    </div>
    <p v-else>
      <span class="text-color">Why not</span>
      <span><a href="/register" class="accent-color">Register</a></span>
      <span class="text-color">or</span>
      <span><a href="/login" class="accent-color">Log In</a></span>
      <span class="text-color">to access all the features and functionalities?</span>
    </p>
  </section>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'HomeView',
  computed: {
    isLoggedIn: function() {
      return this.$store.getters.isAuthenticated;
    }
  },
});
</script>

<style scoped>
.dark-theme {
  background-color: #000000;
  color: #ffd700;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0px 0px 15px 0px #000000;
}

.text-color {
  color: #ffd700;
}

.accent-color {
  color: #ffd700;
  text-decoration: none;
  transition: color 0.2s;
}

.accent-color:hover {
  color: #a89100;
}
</style>
