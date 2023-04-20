<template>
  <div>
    <section>
      <h1>My Images</h1>
      <hr /><br />

      <div v-if="images.length">
        <div class="image-grid">
          <div v-for="image in images" :key="image" @click="selectImage(image)">
            <img
              :src="image"
              :class="{ 'selected-image': selectedImage === image }"
              alt="Image"
            />
          </div>
        </div>
        <div v-if="selectedImage" class="process-btn-container">
          <button @click="processImage" class="process-btn">Process</button>
        </div>
      </div>

      <div v-else>
        <p>No images to display.</p>
      </div>
    </section>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { mapGetters } from 'vuex';
import axios from 'axios';

export default defineComponent({
  name: 'MyImagesView',
  computed: {
    ...mapGetters('auth', ['userId']),
  },
  data() {
    return {
      images: [],
      selectedImage: null,
    };
  },
  methods: {
    selectImage(image) {
      this.selectedImage = image;
    },
    processImage() {
      console.log('Processing image:', this.selectedImage);
      // Add your image processing logic here
    },
  },
  async created() {
    try {
      const response = await axios.get(`/images`);
      this.images = response.data;
    } catch (error) {
      console.error(error);
    }
  },
});
</script>

<style scoped>
.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-gap: 10px;
}

.image-grid img {
  width: 100%;
  height: auto;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.image-grid img.selected-image {
  transform: scale(1.05);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.process-btn-container {
  display: flex;
  justify-content: flex-end;
  position: fixed;
  right: 20px;
  bottom: 20px;
}

.process-btn {
  background-color: #2196f3;
  border: none;
  border-radius: 4px;
  color: white;
  font-size: 16px;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.process-btn:hover {
  background-color: #1976d2;
}
</style>
