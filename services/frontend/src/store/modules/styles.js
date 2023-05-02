import axios from 'axios';

const state = {
  stylesList: [],
  styleImages: {},
  styleImage: null,
  selectedStyle: null,
};

const getters = {
  stylesList: (state) => state.stylesList,
  styleImages: (state) => state.styleImages,
  styleImage: (state) => state.styleImage,
  selectedStyle: (state) => state.selectedStyle,
};

const actions = {
  async getStyles({ commit }) {
    const { data } = await axios.get('styles');
    commit('setStylesList', data);
  },
  async getStyleImages({ commit }, styleName) {
    const { data } = await axios.get(`style/${styleName}/images`);
    commit('setStyleImages', { styleName, images: data });
  },
  async getStyleImage({ commit }, { styleName, imageName }) {
    const response = await axios.get(`style/${styleName}/images/${imageName}`, {
      responseType: 'blob',
    });
    const imageUrl = URL.createObjectURL(response.data);
    commit('setStyleImage', imageUrl);
  },
  setSelectedStyle({ commit }, styleName) {
    commit('setSelectedStyle', styleName);
  },
  // ... (other actions)
};

const mutations = {
  setStylesList(state, styles) {
    state.stylesList = styles.map(style => style.name);
  },
  setStyleImages(state, { styleName, images }) {
    state.styleImages = { ...state.styleImages, [styleName]: images };
  },
  setStyleImage(state, imageUrl) {
    state.styleImage = imageUrl;
  },
  setSelectedStyle(state, styleName) {
    state.selectedStyle = styleName;
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
