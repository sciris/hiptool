<!--
UserChangeInfoPage.vue -- Vue component for a page to change account info

Last update: 3/7/18 (gchadder3)
-->

<template>
  <div class="SitePage">

    <div class="divTable">
      <div class="divTableBody">
        <div class="divTableRow">
          <div class="divRowLabel">Username: </div>
          <div class="divRowContent"><input v-model='changeUserName'/></div>
        </div>
        <div class="divTableRow">
          <div class="divRowLabel">Display name: </div>
          <div class="divRowContent"><input v-model='changeDisplayName'/></div>
        </div>
        <div class="divTableRow">
          <div class="divRowLabel">Email: </div>
          <div class="divRowContent"><input v-model='changeEmail'/></div>
        </div>
        <div class="divTableRow">
          <div class="divRowLabel">Reenter password:</div>
          <div class="divRowContent"><input v-model='changePassword'/></div>
        </div>
      </div>
    </div>

    <button class="btn __green" @click="tryChangeInfo">Update</button>
    <br/>

    <p v-if="changeResult != ''">{{ changeResult }}</p>
  </div>
</template>

<script>
import rpcservice from '@/services/rpc-service'
import router from '@/router'

export default {
  name: 'UserChangeInfoPage',

  data () {
    return {
      changeUserName: this.$store.state.currentUser.username,
      changeDisplayName: this.$store.state.currentUser.displayname,
      changeEmail: this.$store.state.currentUser.email,
      changePassword: '',
      changeResult: ''
    }
  },

  methods: {
    tryChangeInfo () {
      rpcservice.rpcUserChangeInfoCall('user_change_info', this.changeUserName,
        this.changePassword, this.changeDisplayName, this.changeEmail)
      .then(response => {
        if (response.data == 'success') {
          // Set a success result to show.
          this.$notifications.notify({
            message: 'User info updated',
            icon: 'ti-check',
            type: 'success',
            verticalAlign: 'top',
            horizontalAlign: 'center',
          });

          // Read in the full current user information.
          rpcservice.rpcGetCurrentUserInfo('get_current_user_info')
          .then(response2 => {
            // Set the username to what the server indicates.
            this.$store.commit('newUser', response2.data.user)

            // Navigate automatically to the home page.
            router.push('/')
          })
          .catch(error => {
            // Set the username to {}.  An error probably means the
            // user is not logged in.
            this.$store.commit('newUser', {})
          })
        } else {
          // Set a failure result to show.
          this.$notifications.notify({
            message: 'Failed to update user info',
            icon: 'ti-face-sad',
            type: 'danger',
            verticalAlign: 'top',
            horizontalAlign: 'center',
          });
        }
      })
      .catch(error => {
        this.changeResult = 'Server error.  Please try again later.'
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
