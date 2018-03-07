<!-- 
TopBar.vue -- TopBar Vue component

Last update: 3/7/18 (gchadder3)
-->

<template>
  <div class="TopBar">
    <div class="elastic header">
      <div style="display:table-cell; width:160px">
        <img src="../assets/images/healthpriorlogo.png" height="50">
      </div>

      <div style="display:table-cell; vertical-align: middle;" v-if="userloggedin()">
        <div class="menu">
          <router-link v-if="adminloggedin()" 
                       tag="div" 
                       to="/mainadmin" 
                       class="menu-item" 
                       :class="{'menu-active': $route.path === '/mainadmin'}">
            Admin
          </router-link>

          <router-link tag="div" 
                       to="/" 
                       class="menu-item" 
                       :class="{'menu-active': $route.path === '/'}">
            Manage projects
          </router-link>

          <router-link tag="div" 
                       to="/bod" 
                       class="menu-item" 
                       :class="{'menu-active': $route.path === '/bod'}">
            Burden of disease
          </router-link>

          <router-link tag="div" 
                       to="/interventions" 
                       class="menu-item" 
                       :class="{'menu-active': $route.path === '/interventions'}">
            Interventions
          </router-link>

          <router-link tag="div" 
                       to="/healthpackages" 
                       class="menu-item" 
                       :class="{'menu-active': $route.path === '/healthpackages'}">
            Define health packages
          </router-link>

<!--          <div class="menu-item">
            <router-link to="/mypage" tag="span">
              Old main
            </router-link> 
          </div> -->

          <router-link tag="div" 
                       to="/changeinfo" 
                       class="menu-item" 
                       :class="{'menu-active': $route.path === '/changeinfo'}">
            Edit account
          </router-link>

          <router-link tag="div" 
                       to="/changepassword" 
                       class="menu-item" 
                       :class="{'menu-active': $route.path === '/changepassword'}">
            Change password
          </router-link>

          <div class="menu-item">
            Help
          </div>

          <div class="menu-item" @click="logout">
            Logout
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import rpcservice from '../services/rpc-service'
import router from '../router'

export default {
  name: 'TopBar', 

  data() {
    return {
      activePage: 'manage projects'
    }
  },

  computed: {
    currentUser() {
      return this.$store.state.currentUser
    }
  },

  created() {
    this.getUserInfo()
  },

  methods: {
    userloggedin() {
      if (this.currentUser.displayname == undefined) 
        return false
      else
        return true
    }, 

    adminloggedin() {
      if (this.userloggedin) {
        return this.currentUser.admin
      }
    },

    logout() {
      // Do the logout request.
      rpcservice.rpcLogoutCall('user_logout')
      .then(response => {
        // Update the user info.
        this.getUserInfo()

        // Navigate to the login page automatically.
        router.push('/login')
      })
    },

    getUserInfo() {
      rpcservice.rpcGetCurrentUserInfo('get_current_user_info')
      .then(response => {
        // Set the username to what the server indicates.
        this.$store.commit('newUser', response.data.user)
      })
      .catch(error => {
        // Set the username to {}.  An error probably means the 
        // user is not logged in.
        this.$store.commit('newUser', {})
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
