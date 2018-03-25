<!--
User registration page

Last update: 2018mar25
-->

<template>
  <div class="SitePage" style="width: 500px; margin:auto">

    <div class="divTable">
      <div class="divTableBody">
        <div class="divTableRow">
          <div class="divRowLabel">Username: </div>
          <div class="divRowContent"><input v-model='registerUserName'/></div>
        </div>
        <div class="divTableRow">
          <div class="divRowLabel">Password:</div>
          <div class="divRowContent"><input v-model='registerPassword'/></div>
        </div>
        <div class="divTableRow">
          <div class="divRowLabel">Display name: </div>
          <div class="divRowContent"><input v-model='registerDisplayName'/></div>
        </div>
        <div class="divTableRow">
          <div class="divRowLabel">Email: </div>
          <div class="divRowContent"><input v-model='registerEmail'/></div>
        </div>
      </div>
    </div>

    <button class="btn __green" @click="tryRegister">Register</button>
    <br/>

    <p v-if="registerResult != ''">{{ registerResult }}</p>

    Already have an account?
    <router-link to="/login">
        Log in
    </router-link>
  </div>
</template>

<script>
import rpcservice from '@/services/rpc-service'
import router from '@/router'

export default {
  name: 'RegisterPage',

  data () {
    return {
      registerUserName: '',
      registerPassword: '',
      registerDisplayName: '',
      registerEmail: '',
      registerResult: ''
    }
  },

  methods: {
    tryRegister () {
      rpcservice.rpcRegisterCall('user_register', this.registerUserName,
        this.registerPassword, this.registerDisplayName, this.registerEmail)
      .then(response => {
        if (response.data == 'success') {
          this.registerResult = 'Success';
          // Set a success result to show.
          // CK: Can't show these since don't appear here
//          this.$notifications.notify({
//            message: 'Registered!',
//            icon: 'ti-check',
//            type: 'success',
//            verticalAlign: 'top',
//            horizontalAlign: 'center',
//          });

          // Navigate automatically to the login page.
          router.push('/login')
        } else {
          // Set a failure result to show.
          this.registerResult = 'Failure';
//          this.$notifications.notify({
//            message: 'Failed to register',
//            icon: 'ti-face-sad',
//            type: 'danger',
//            verticalAlign: 'top',
//            horizontalAlign: 'center',
//          });
        }
      })
      .catch(error => {
        this.registerResult = 'Server error.  Please try again later.'
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
