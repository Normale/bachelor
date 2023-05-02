import { createStore } from "vuex";

import notes from './modules/notes';
import users from './modules/users';
import images from './modules/images';
import styles from './modules/styles';

export default createStore({
  modules: {
    notes,
    users,
    images,
    styles
  }
});
