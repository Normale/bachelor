<template>
  <div id="app">
    <NavBar />
    <div class="main container">
      <router-view />
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
export default {
  components: {
    NavBar,
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono&display=swap');

html,
body {
  height: 100%;
  margin: 0;
}

#app {
  font-family: 'Roboto Mono', monospace;
  font-size: 18px;
  color: #ffd700;
  background-color: #000000;
  min-height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  border-radius: 20px;
  padding: 20px;
  box-shadow: 0px 0px 15px 0px #000000;
}

.main {
  padding-top: 5em;
  width: 80%;
  border-radius: 20px;
  background-color: #000000;
  padding: 20px;
  box-shadow: 0px 0px 15px 0px #000000;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  border-radius: 20px;
  overflow: hidden;
}

a {
  color: #ffd700;
  transition: color 0.2s;
}

a:hover {
  color: #000000;
}

button {
  background-color: #ffd700;
  color: #000000;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #a89100;
}

input[type="text"],
input[type="email"],
textarea {
  background-color: #000000;
  border: none;
  border-radius: 5px;
  color: #ffd700;
  padding: 10px;
}

input[type="text"]:focus,
input[type="email"]:focus,
textarea:focus {
  outline: none;
  box-shadow: 0px 0px 5px 0px #ffd700;
}

select {
  background-color: #000000;
  border: none;
  border-radius: 5px;
  color: #ffd700;
  padding: 10px;
}

option {
  background-color: #000000;
}
</style>
