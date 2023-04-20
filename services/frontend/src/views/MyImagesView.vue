<template>
    <div>
      <section>
        <h1>My Images</h1>
        <hr/><br/>
  
        <div v-if="images.length">
          <div v-for="image in images" :key="image">
            <img :src="image" alt="Image" style="max-width: 100%; max-height: 300px;" />
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
    };
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
