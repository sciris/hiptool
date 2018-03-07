// index.js -- Vuex store configuration
//
// Last update: 3/7/18 (gchadder3)

import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    currentUser: {}
  },

  mutations: {
    newUser(state, user) {
      state.currentUser = user
    }
  }
})
export default store