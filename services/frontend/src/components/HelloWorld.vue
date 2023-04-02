<!-- HelloWorld.vue -->
<template>
  <div class="ping-container">
    <p class="ping-message">{{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'Ping',
  data() {
    return {
      msg: '',
    };
  },
  methods: {
    getMessage() {
      axios.get('/')
        .then((res) => {
          this.msg = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getMessage();
  },
});

<style scoped>
.ping-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #000000;
}

.ping-message {
  font-size: 48px;
  font-weight: bold;
  color: #ffd700;
  text-shadow: 2px 2px #000000;
}
</style>

