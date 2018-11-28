<!--
Definition of the dashboard itself

Last update: 2018-08-16
-->

<template>
  <div class="wrapper">
    <sidebar 
      style="background-color: #212120;"
      :links="sidebarLinks"
      type="sidebar" 
      logoWidth="130px"
      logo="/static/img/healthpriorlogo-inverse.png"
      favicon="/static/favicon-96x96.png"> 
    </sidebar>
    <notifications></notifications>

    <div class="main-panel">
      <navbar showRouteName="true"></navbar>
      <dashboard-content @click.native="toggleSidebar"></dashboard-content>
      <content-footer></content-footer>
    </div>
  </div>
</template>
<script>
import sciris from 'sciris-js';
import ContentFooter from './ContentFooter.vue'
import DashboardContent from './Content.vue'

export default {
  components: {
    ContentFooter,
    DashboardContent
  },
  computed: {
    sidebarLinks(){
      console.log(this.$store.state.sidebarLinks)
      return this.$store.state.sidebarLinks
    },
    navbarLinks(){
      return this.$store.state.navbarLinks;
    },
  },
  methods: {
    toggleSidebar () {
      if (this.$sidebar.showSidebar) {
        this.$sidebar.displaySidebar(false)
      }
    }
  }
}
</script>
