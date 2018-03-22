<!--
RegisterPage.vue -- RegisterPage Vue component

Last update: 2/13/18 (gchadder3)
-->

<template>
  <div class="SitePage" style="width: 500px">
    <span class="text_bold_medium" style="width: 25%">Username</span>
    <input v-model='registerUserName' style="width: 100%" class="txbox __l"/>
    <br/>

    <span class="text_bold_medium" style="width: 25%">Password:</span>
    <input v-model='registerPassword' style="width: 100%" class="txbox __l"/>
    <br/>

    <span class="text_bold_medium" style="width: 25%">Display name:</span>
    <input v-model='registerDisplayName' style="width: 100%" class="txbox __l"/>
    <br/>

    <span class="text_bold_medium" style="width: 25%">Email:</span>
    <input v-model='registerEmail' style="width: 100%" class="txbox __l"/>
    <br/>

    <button @click="tryRegister" class="section btn __l __block">Register</button>
    <br/>

    <p v-if="registerResult != ''">{{ registerResult }}</p>

    Already have an account?
    <router-link to="/login">
        Log in
    </router-link>
  </div>
</template>

<script>
import rpcservice from '../services/rpc-service'
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
          // Set a success result to show.
          this.registerResult = 'Success!'

          // Navigate automatically to the login page.
          router.push('/login')
        } else {
          // Set a failure result to show.
          this.registerResult = 'Registration failed.  Try again, possibly with a different username.'
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
