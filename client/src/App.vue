<!-- 
App.vue -- App component, the main page

Last update: 2/2/18 (gchadder3)
-->

<template>
  <div :class="{'nav-open': $sidebar.showSidebar}">
    <router-view></router-view>
    <!--This sidebar appears only for screens smaller than 992px-->
    <side-bar type="navbar" :sidebar-links="$sidebar.sidebarLinks">
      <ul class="nav navbar-nav">
        <!-- Below requires a userService -->
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
        <li class="divider"></li>
      </ul>
    </side-bar>
  </div>
  
</template>

<script>
import userService from '@/services/user-service'

export default {
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
  }

}

</script>

<!-- Global SCSS/SASS settings go here. -->
<style lang="scss">
  // @import './sass/main.scss';

/* #app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */
</style>
