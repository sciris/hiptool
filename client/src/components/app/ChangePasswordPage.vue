<!--
Change the user's password

Last update: 2018mar25
-->

<template>
  <div class="SitePage">

    <div class="divTable">
      <div class="divTableBody">
        <div class="divTableRow">
          <div class="divRowLabel">Reenter old password:</div>
          <div class="divRowContent"><input v-model='oldPassword'/></div>
        </div>
        <div class="divTableRow">
          <div class="divRowLabel">Enter new password: </div>
          <div class="divRowContent"><input v-model='newPassword'/></div>
        </div>
      </div>
    </div>

    <button class="btn __green" @click="tryChangePassword">Update</button>
    <br/>

    <p v-if="changeResult != ''">{{ changeResult }}</p>
  </div>
</template>

<script>
import rpcservice from '@/services/rpc-service'
import router from '@/router'

export default {
  name: 'ChangePasswordPage',

  data () {
    return {
      oldPassword: '',
      newPassword: '',
      changeResult: ''
    }
  },

  methods: {
    tryChangePassword () {
      rpcservice.rpcChangePasswordCall('user_change_password', this.oldPassword,
        this.newPassword)
      .then(response => {
        if (response.data == 'success') {
          // Set a success result to show.
          this.$notifications.notify({
            message: 'Password updated',
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
            message: 'Password update failed',
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
