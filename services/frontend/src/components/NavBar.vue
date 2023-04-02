<template>
  <header>
    <nav class="navbar navbar-expand-md navbar-dark bg-gold">
      <div class="container">
        <a class="navbar-brand" href="/">
          <img class="navbar-logo" src="https://source.unsplash.com/random/50x50" alt="Logo">
          FastAPI + Vue
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
          <ul v-if="isLoggedIn" class="navbar-nav ms-auto mb-2 mb-md-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/" >
                <span class="nav-link-underline">Home</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/dashboard">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/profile">My Profile</router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link nav-link-button" @click="logout">Log Out</a>
            </li>
          </ul>
          <ul v-else class="navbar-nav ms-auto mb-2 mb-md-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/">
                <span class="nav-link-underline">Home</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/register">
                <span class="nav-link-underline">Register</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/login">
                <span class="nav-link-underline nav-link-login">Log In</span>
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'NavBar',
  computed: {
    isLoggedIn() {
      return this.$store.getters.isAuthenticated;
    }
  },
  methods: {
    async logout() {
      await this.$store.dispatch('logOut');
      this.$router.push('/login');
    }
  },
});
</script>


<style scoped>
.navbar {
  height: 80px;
  background-color: #000000;
  color: #ffd700;
}

.navbar-brand {
  font-size: 28px;
  display: flex;
  align-items: center;
}

.navbar-logo {
  height: 50px;
  width: 50px;
  margin-right: 10px;
  border-radius: 50%;
  object-fit: cover;
}

.nav-link {
  font-size: 20px;
  padding: 15px;
}

.nav-link-underline {
  position: relative;
  text-decoration: none;
}

.nav-link-underline::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -5px;
  width: 0%;
  height: 2px;
  background-color: #ffd700;
  transition: width 0.3s ease-in-out;
}

.nav-link-underline:hover::after {
  width: 100%;
}

.nav-link-login {
  border: 2px solid #ffd700;
  border-radius: 20px;
  padding: 10px 20px;
  transition: all 0.3s ease-in-out;
}

.nav-link-login:hover {
  background-color: #ffd700;
  color: #000000;
}
</style>