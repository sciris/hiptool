export default {
  data() {
    return {
      showSidebar: false
    }
  },
  methods: {
    displaySidebar: function (value) {
      this.$store.commit('changeToggleStatus')
      console.log(this.$store.state.menuToggle)
    }
  }
}
