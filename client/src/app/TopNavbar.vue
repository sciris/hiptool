<!--
Definition of top navigation bar

Last update: 2018sep22
-->

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
        <!-- If you edit this section, make sure to fix the section in App.vue for the narrow screen -->
        <ul class="nav navbar-nav navbar-right">
          <li>
            <router-link to="/projects">
              <i class="ti-view-grid"></i>
              <p>
                Project: <span>{{ activeProjectName }}</span>
              </p>
            </router-link>
          </li>
          <drop-down v-bind:title="activeUserName" icon="ti-user">
            <li><a href="#/changeinfo"><i class="ti-pencil"></i>&nbsp;&nbsp;Edit account</a></li>
            <li><a href="#/changepassword"><i class="ti-key"></i>&nbsp;&nbsp;Change password</a></li>
            <li><a href="#" v-on:click=logOut()><i class="ti-car"></i>&nbsp;&nbsp;Log out</a></li>
          </drop-down>
        </ul>
      </div>
    </div>
  </nav>
</template>


<script>
  import userservice from '@/js/user-service'
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
      currentUser(){
        return userservice.currentUser()
      },

      activeProjectName() {
        if (this.$store.state.activeProject.project === undefined) {
          return 'none'
        } else {
          return this.$store.state.activeProject.project.name
        }
      },

      activeUserName() {
        // Get the active user name -- the display name if defined; else the user name
        var username = userservice.currentUser().username;
        var dispname = userservice.currentUser().displayname;
        var userlabel = '';
        if (dispname === undefined || dispname === '') {
          userlabel = username;
        } else {
          userlabel = dispname;
        }
        return 'User: '+userlabel
      },

      // Theme function
      routeName () {
        const route_name = this.$route.name
        return this.capitalizeFirstLetter(route_name)
      },
    },

    // Health prior function
    created() {
      userservice.getUserInfo()
    },

    // Theme function
    data () {
      return {
        activeNotifications: false
      }
    },
    methods: {
      // Health prior functions
      checkLoggedIn() {
        userservice.checkLoggedIn
      },

      checkAdminLoggedIn() {
        userservice.checkAdminLoggedIn
      },

      logOut() {
        userservice.logOut()
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
