<template>
  <div>
    <section>
      <h1>Upload Image</h1>
      <hr/><br/>

      <form @submit.prevent="submit">
        <div class="mb-3">
          <label for="image" class="form-label">Image:</label>
          <input type="file" name="image" accept="image/*" @change="onImageSelected" class="form-control" />
        </div>
        <button type="submit" class="btn btn-primary" :disabled="!form.imageFile">Submit</button>
        
      </form>
    </section>

    <br/><br/>

    <section>
      <h1>Preview</h1>
      <hr/><br/>

      <div v-if="form.image">
        <img :src="form.image" alt="Preview" style="max-width: 100%; max-height: 300px;" />
      </div>

      <div v-else>
        <p>No image selected.</p>
      </div>
    </section>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { mapActions } from 'vuex';

export default defineComponent({
  name: 'DashboardView',
  data() {
    return {
      form: {
        image: null,
        imageFile: null,
      },
    };
  },
  methods: {
    ...mapActions('images', ['uploadImage']),
    async submit() {
      await this.uploadImage(this.form);
    },
    onImageSelected(event) {
      this.form.image = URL.createObjectURL(event.target.files[0]);
      this.form.imageFile = event.target.files[0];
    },
  },
});
</script>
