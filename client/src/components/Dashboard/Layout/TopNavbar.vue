<template>
  <nav class="navbar navbar-default">
    <div class="container-fluid">
      <div class="navbar-header">
        <button type="button" class="navbar-toggle" :class="{toggled: $sidebar.showSidebar}" @click="toggleSidebar">
          <span class="sr-only">Toggle navigation</span>
          <span class="icon-bar bar1"></span>
          <span class="icon-bar bar2"></span>
          <span class="icon-bar bar3"></span>
        </button>
        <a class="navbar-brand">{{routeName}}</a>
      </div>
      <div class="collapse navbar-collapse">
        <ul class="nav navbar-nav navbar-right">
          <li class="open">
            <a href="#" class="dropdown-toggle btn-magnify" data-toggle="dropdown">
              <i class="ti-panel"></i>
              <p>Stats</p>
            </a>
          </li>
             <drop-down title="5 Notifications" icon="ti-bell">
               <li><a href="#">Notification 1</a></li>
               <li><a href="#">Notification 2</a></li>
               <li><a href="#">Notification 3</a></li>
               <li><a href="#">Notification 4</a></li>
               <li><a href="#">Another notification</a></li>
             </drop-down>
          <li>
            <a href="#" class="btn-rotate">
              <i class="ti-settings"></i>
              <p>
                Settings
              </p>
            </a>
          </li>
          <li>
            <a href="#" class="btn-rotate" @click="logout">
              <i class="ti-close"></i>
              <p>
                Log out
              </p>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
  import rpcservice from '@/services/rpc-service'
  import router from '@/router'

  export default {
    name: 'TopBar', 

    // Health prior function
    data() {
      return {
        activePage: 'manage projects'
      }
    },

    computed: {
      // Health prior function
      currentUser() {
        return this.$store.state.currentUser
      },

      // Theme function
      routeName () {
        const {name} = this.$route
        return this.capitalizeFirstLetter(name)
      }
    },

    // Health prior function
    created() {
      this.getUserInfo()
    },

    // Theme function
    data () {
      return {
        activeNotifications: false
      }
    },
    methods: {
      // Health prior functions
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

          // Clear out the active project.
          this.$store.commit('newActiveProject', {})

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
      },

      // Theme functions
      capitalizeFirstLetter (string) {
        return string.charAt(0).toUpperCase() + string.slice(1)
      },
      toggleNotificationDropDown () {
        this.activeNotifications = !this.activeNotifications
      },
      closeDropDown () {
        this.activeNotifications = false
      },
      toggleSidebar () {
        this.$sidebar.displaySidebar(!this.$sidebar.showSidebar)
      },
      hideSidebar () {
        this.$sidebar.displaySidebar(false)
      }
    }
  }

</script>
<style>

</style>
