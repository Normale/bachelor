<template>
  <div>
    <h1>Process Image</h1>
    <div v-if="selectedImage">
      <div class="options">
        <label v-for="style in stylesList" :key="style">
          <input type="radio" :id="style" :value="style" v-model="selectedStyle" @change="fetchStyleImages" />{{ style }}
        </label>
      </div>
      <div class="images-container">
        <img :src="selectedImage" alt="Selected image" class="processed-image" />
        <img v-if="selectedStyleImage" :src="selectedStyleImage" alt="Selected style image" class="processed-image" />
        <img v-if="resultImageUrl" :src="resultImageUrl" alt="Result image" class="processed-image" />
        <div v-if="processing">
          <p>Processing... Estimated time: {{ estimatedTime }} seconds</p>
        </div>
      </div>
      <div class="gallery">
        <img v-for="image in (styleImages[selectedStyle] ? Object.values(styleImages[selectedStyle]) : [])" :key="image"
          :src="image" alt="Style image" class="gallery-image" @click="selectStyleImage(image)" />
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
      selectedStyleImage: '',
      websocket: null,
      processing: false,
      estimatedTime: 0,
      resultImageUrl: '',
    };
  },
  methods: {
    ...mapActions('styles', ['getStyles', 'getStyleImages']),
    async fetchStyleImages() {
      const images = await this.getStyleImages(this.selectedStyle);
      this.styleImages = images.map(image => image.url);
    },
    selectStyleImage(image) {
      this.selectedStyleImage = image;
    },
    generate() {
      console.log('Generate button clicked');
      console.log('Selected Image:', this.selectedImage);
      console.log('Selected Style Image:', this.selectedStyleImage);
      this.sendDataToServer();
    },
    sendDataToServer() {
      if (!this.websocket) {
        // Replace the URL with your WebSocket server's URL
        this.websocket = new WebSocket('ws://localhost:5000/ws');
      }

      this.websocket.addEventListener('open', () => {
        const data = {
          selectedImage: this.selectedImage,
          selectedStyleImage: this.selectedStyleImage,
          selectedStyle: this.selectedStyle,
        };

        this.websocket.send(JSON.stringify(data));
      });

      this.websocket.addEventListener('message', (event) => {
        console.log('Server response:', event.data);
        const responseData = JSON.parse(event.data);

        if (responseData.state === 'processing') {
          this.processing = true;
          this.estimatedTime = responseData.details.estimated_time;
        } else if (responseData.state === 'finished') {
          this.processing = false;
          this.resultImageUrl = responseData.result;
        }
      });

      this.websocket.addEventListener('message', (event) => {
        console.log('Server response:', event.data);
        // Handle the server response here
      });

      this.websocket.addEventListener('error', (event) => {
        console.error('WebSocket error:', event);
      });

      this.websocket.addEventListener('close', () => {
        console.log('WebSocket closed');
      });
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
