import axios from 'axios';

const state = {
  images: null,
  image: null,
};

const getters = {
  stateImages: (state) => state.images,
  stateImage: (state) => state.image,
};

const actions = {
  async uploadImage({ dispatch }, imageForm) {
    const formData = new FormData();
    formData.append('image', imageForm.imageFile);

    await axios.post('images', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    await dispatch('getImages');
  },
  async getImages({ commit }) {
    const { data } = await axios.get('images');
    commit('setImages', data);
  },
  // ... (other actions)
};

const mutations = {
  setImages(state, images) {
    state.images = images;
  },
  setImage(state, image) {
    state.image = image;
  },
  // ... (other mutations)
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
};
