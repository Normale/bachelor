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
        <img v-if="resultImageUrl" :src="resultImageUrl" alt="Result image" class="processed-image result-image" />
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
      if (!this.websocket || this.websocket.readyState !== WebSocket.OPEN) {
        this.websocket = new WebSocket('ws://localhost:5000/ws');

        this.websocket.addEventListener('open', () => {
          this.sendImageDetails();
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

        this.websocket.addEventListener('error', (event) => {
          console.error('WebSocket error:', event);
        });

        this.websocket.addEventListener('close', () => {
          console.log('WebSocket closed');
        });
      } else {
        this.sendImageDetails();
      }
    },
    sendImageDetails() {
      const data = {
        selectedImage: this.selectedImage,
        selectedStyleImage: this.selectedStyleImage,
        selectedStyle: this.selectedStyle,
      };

      this.websocket.send(JSON.stringify(data));
    },
  },

  mounted() {
    this.getStyles();
  },
});
</script>




<style scoped>
.images-container {
  display: flex;
  /* Convert container into a flex container */
  justify-content: space-between;
  /* Distribute space between the images */
  align-items: center;
  /* Center align vertically */
  flex-wrap: wrap;
  /* Allow items to wrap to the next line if needed */
  gap: 1rem;
  /* Space between each image */
}

.result-image {
  max-width: 50%;
  /* Making it larger. Adjust as needed */
  max-height: 400px;
  /* Adjust the height if needed */
  border: 3px solid #007bff;
  /* Adding a border. Change the color and width as desired */
  margin: 1rem 0;
  /* Add some vertical margin */
  flex: 2;
  /* Allows the image to grow more than the other images, making it larger in the flex layout */
}


.processed-image {
  max-width: calc(25% - 1rem);
  /* Adjust max-width to fit three images. Subtracting the gap size */
  max-height: 300px;
  margin-bottom: 1rem;
  flex: 1;
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
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 1000;
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
