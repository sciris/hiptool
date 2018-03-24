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
      name: 'Help',
      icon: 'ti-help',
      path: '/admin/help'
    },
    {
      name: 'Contact',
      icon: 'ti-comment-alt',
      path: '/admin/contact'
    },
    {
      name: 'About',
      icon: 'ti-face-smile',
      path: '/admin/about'
    },
  ],

  displaySidebar (value) {
    this.showSidebar = value
  },
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
