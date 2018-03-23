import Sidebar from './SideBar.vue'

const SidebarStore = {
  showSidebar: false,
  sidebarLinks: [
    {
      name: 'Projects',
      icon: 'ti-view-grid',
      path: '/admin/projects'
    },
    {
      name: 'Burden of disease',
      icon: 'ti-bar-chart',
      path: '/admin/bod'
    },
    {
      name: 'Interventions',
      icon: 'ti-bolt',
      path: '/admin/interventions'
    },
    {
      name: 'Health packages',
      icon: 'ti-heart',
      path: '/admin/healthpackages'
    },
    {
      name: 'Edit account',
      icon: 'ti-user',
      path: '/admin/changeinfo'
    },
    {
      name: 'Change password',
      icon: 'ti-shield',
      path: '/admin/changepassword'
    }
  ],
  displaySidebar (value) {
    this.showSidebar = value
  }
}

const SidebarPlugin = {

  install (Vue) {
    Vue.mixin({
      data () {
        return {
          sidebarStore: SidebarStore
        }
      }
    })

    Object.defineProperty(Vue.prototype, '$sidebar', {
      get () {
        return this.$root.sidebarStore
      }
    })
    Vue.component('side-bar', Sidebar)
  }
}

export default SidebarPlugin
