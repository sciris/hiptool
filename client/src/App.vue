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
        <li>
          <a class="dropdown-toggle" data-toggle="dropdown">
            <i class="ti-panel"></i>
            <p>Stats</p>
          </a>
        </li>
        <drop-down title="5 Notifications" icon="ti-bell">

          <li><a>Notification 1</a></li>
          <li><a>Notification 2</a></li>
          <li><a>Notification 3</a></li>
          <li><a>Notification 4</a></li>
          <li><a>Another notification</a></li>

        </drop-down>
        <li>
          <a>
            <i class="ti-settings"></i>
            <p>Settings</p>
          </a>
        </li>
        <li class="divider"></li>
      </ul>
    </side-bar>
  </div>
  
</template>

<script>
export default {}

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
