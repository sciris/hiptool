import rpcservice from '@/services/rpc-service'
import store from './../store'
var state = {
  currentUser: {}
};

export default {
  currentUser() {
    return store.state.currentUser
  },

  getUserInfo() {
    rpcservice.rpcGetCurrentUserInfo('get_current_user_info')
    .then(response => {
      // Set the username to what the server indicates.
      store.commit('newUser', response.data.user)
    })
    .catch(error => {
      // Set the username to {}.  An error probably means the
      // user is not logged in.
      store.commit('newUser', {})
    })
  },

  checkLoggedIn () {
    if (this.currentUser.displayname == undefined)
      return false
    else
      return true
  },

  checkAdminLoggedIn() {
    if (this.checkLoggedIn) {
      return this.currentUser.admin
    }
  },

}