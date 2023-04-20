<!-- src/views/ProcessImage.vue -->
<template>
    <div>
      <h1>Process Image</h1>
      <div v-if="selectedImage">
        <div class="options">
          <label>
            <input
              type="radio"
              id="optionA"
              value="a"
              v-model="selectedOption"
            />Option A
          </label>
          <label>
            <input
              type="radio"
              id="optionB"
              value="b"
              v-model="selectedOption"
            />Option B
          </label>
        </div>
        <img :src="selectedImage" alt="Selected image" class="processed-image" />
        <div class="generate-btn-container">
          <button @click="generate" class="generate-btn">Generate</button>
        </div>
      </div>
      <div v-else>
        <p>No image selected. Please go back and select an image.</p>
      </div>
    </div>
  </template>
  
  <script>
  import { defineComponent } from 'vue';
  import { mapGetters } from 'vuex';
  
  export default defineComponent({
    name: 'ProcessImageView',
    computed: {
      ...mapGetters('images', ['selectedImage']),
    },
    data() {
      return {
        selectedOption: 'a',
      };
    },
    methods: {
      generate() {
        console.log('Generate button clicked');
        // Add your generate functionality here
      },
    },
  });
  </script>
  
  <style scoped>
  .processed-image {
    max-width: 100%;
    max-height: 300px;
    display: block;
    margin-bottom: 1rem;
  }
  
  .options {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-bottom: 1rem;
  }
  
  .options label {
    cursor: pointer;
  }
  
  .generate-btn-container {
    display: flex;
    justify-content: flex-end;
  }
  
  .generate-btn {
    background-color: #007bff;
    color: #fff;
    border: none;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    cursor: pointer;
    border-radius: 0.25rem;
    transition: background-color 0.2s;
  }
  
  .generate-btn:hover {
    background-color: #0056b3;
  }
  </style>
  