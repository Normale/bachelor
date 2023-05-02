<template>
  <div>
    <h1>Process Image</h1>
    <div v-if="selectedImage">
      <div class="options">
        <label v-for="style in stylesList" :key="style">
          <input type="radio" :id="style" :value="style" v-model="selectedStyle" @change="fetchStyleImages" />{{ style }}
        </label>
      </div>
      <img :src="selectedImage" alt="Selected image" class="processed-image" />
      <div class="gallery">
        <img
  v-for="image in (styleImages[selectedStyle] ? Object.values(styleImages[selectedStyle]) : [])"
  :key="image"
  :src="image"
  alt="Style image"
  class="gallery-image"
/>

      </div>
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
import { mapGetters, mapActions } from 'vuex';

export default defineComponent({
  name: 'ProcessImageView',
  computed: {
    ...mapGetters('images', ['selectedImage']),
    ...mapGetters('styles', ['stylesList', 'styleImages']),
  },
  data() {
    return {
      selectedStyle: '',
    };
  },
  methods: {
    ...mapActions('styles', ['getStyles', 'getStyleImages']),
    async fetchStyleImages() {
      const images = await this.getStyleImages(this.selectedStyle);
      this.styleImages = images.map(image => image.url);
    },
    generate() {
      console.log('Generate button clicked');
      // Add your generate functionality here
    },
  },

  mounted() {
    this.getStyles();
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

.gallery {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
  margin-bottom: 1rem;
}

.gallery-image {
  max-width: 150px;
  max-height: 150px;
  object-fit: cover;
  border-radius: 0.25rem;
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
