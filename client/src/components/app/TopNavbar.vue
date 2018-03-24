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
        <!-- If you edit this section, make sure to fix the section in App.vue -->
        <ul class="nav navbar-nav navbar-right">
          <li>
            <a href="#" class="btn-rotate">
              <i class="ti-view-grid"></i>
              <p>
                <b>Project: </b><span>{{ activeProjectName }}</span>
              </p>
            </a>
          </li>
          <drop-down v-bind:title="currentUser.username" icon="ti-user">
            <li><a href="#/admin/changeinfo"><i class="ti-pencil"></i>&nbsp;Edit account</a></li>
            <li><a href="#/admin/changepassword"><i class="ti-shield"></i>&nbsp;Change password</a></li>
            <li><a href="#"><i class="ti-car"></i>&nbsp;Log out</a></li>
          </drop-down>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
  import rpcservice from '@/services/rpc-service'
  import userService from '@/services/user-service'
  import router from '@/router'

  export default {
    name: 'TopNavbar',

    // Health prior function
    data() {
      return {
        activePage: 'manage projects'
      }
    },

    computed: {
      // Health prior function
      currentUser: () => {
        return userService.currentUser()
      },

      activeProjectName() {
        if (this.$store.state.activeProject.project === undefined) {
          return 'none'
        } else {
          return this.$store.state.activeProject.project.name
        }
      },

      // Theme function
      routeName () {
        const {name} = this.$route
        return this.capitalizeFirstLetter(name)
      }
    },

    // Health prior function
    created() {
      userService.getUserInfo()
    },

    // Theme function
    data () {
      return {
        activeNotifications: false
      }
    },
    methods: {
      // Health prior functions
      checkLoggedIn: userService.checkLoggedIn,

      checkAdminLoggedIn: userService.checkAdminLoggedIn,

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
