import { createStore } from "vuex";

import notes from './modules/notes';
import users from './modules/users';
import images from './modules/images';

export default createStore({
  modules: {
    notes,
    users,
    images
  }
});
