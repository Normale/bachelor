<template>
    <div>
      <h1>Process Image</h1>
      <div v-if="selectedImage">
        <div>
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
});
</script>
  
<style scoped>
.processed-image {
    max-width: 100%;
    max-height: 300px;
    display: block;
    margin-bottom: 1rem;
}
</style>
  