import axios from 'axios';

const user = JSON.parse(localStorage.getItem('user'));
const state = {
  user: user ? user : null,
};


const getters = {
  isAuthenticated: state => !!state.user,
  stateUser: state => state.user,
};

const actions = {
  async register({ dispatch }, form) {
    await axios.post('register', form);
    let UserForm = new FormData();
    UserForm.append('username', form.username);
    UserForm.append('password', form.password);
    await dispatch('logIn', UserForm);
  },
  async logIn({ dispatch }, user) {
    await axios.post('login', user);
    await dispatch('viewMe');
  },
  async viewMe({ commit }) {
    let { data } = await axios.get('users/whoami');
    await commit('setUser', data);
    localStorage.setItem('user', JSON.stringify(data));
  },
  async deleteUser(_, id) {
    await axios.delete(`user/${id}`);
  },
  async logOut({ commit }) {
    let user = null;
    commit('logout', user);
    localStorage.removeItem('user');
  }
};

const mutations = {
  setUser(state, user) {
    state.user = user;
  },
  logout(state, user) {
    state.user = user;
  },
};

export default {
  state,
  getters,
  actions,
  mutations
};
