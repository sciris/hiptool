<!--
User registration page

Last update: 2018-05-28
-->


<template>
  <div class="SitePage" style="background-color:#f8f8f4; position:fixed; min-height:100%; min-width:100%; padding:0 0 0 0" v-model="getVersionInfo"> <!-- Should match _variables.scss:$bg-nude -->
    <div style="background-color:#212120; position:absolute; height:100%; width:260px">
      <div class="logo">
        <div class="simple-text" style="font-size:20px; color:#fff; font-weight:bold; padding:20px">
          <div class="logo-img" style="height:40px; width:40px; line-height:40px; border-radius:40px; background-color:#fff; text-align:center; display:inline-block">
            <img src="static/favicon-96x96.png" width="21px" vertical-align="middle" alt>
          </div>
          <span style="padding-left:10px">
            <img src="static/img/hiptool-logo-dark-small.png" width="130px" vertical-align="middle" alt>
          </span>
          <br/><br/>
          <div style="font-size:14px; font-weight:normal">
            Version {{ version }} ({{ date }})
          </div>
        </div>
      </div>
    </div>
    <div style="margin-right:-260px">
      <form name="RegisterForm" @submit.prevent="tryRegister" style="max-width: 500px; min-width: 100px; margin: 0 auto">

        <div class="modal-body">
          <h2>Register</h2>

          <div class="section" v-if="registerResult != ''">{{ registerResult }}</div>

          <div class="section form-input-validate">
            <input class="txbox __l"
                   type="text"
                   name="username"
                   placeholder="User name"
                   required="required"
                   v-model='registerUserName'/>
          </div>

          <div class="section form-input-validate">
            <input class="txbox __l"
                   type="password"
                   name="password"
                   placeholder="Password"
                   required="required"
                   v-model='registerPassword'/>
          </div>

          <div class="section form-input-validate">
            <input class="txbox __l"
                   type="text"
                   name="displayname"
                   placeholder="Display name (optional)"
                   v-model='registerDisplayName'/>
          </div>

          <div class="section form-input-validate">
            <input class="txbox __l"
                   type="text"
                   name="email"
                   placeholder="Email (optional)"
                   v-model='registerEmail'/>
          </div>

          <button type="submit" class="section btn __l __block">Register</button>

          <div class="section">
            Already registered?
            <router-link to="/login">
              Login
            </router-link>
          </div>

        </div>
      </form>
    </div>
  </div>
</template>


<script>
import rpcs from '@/js/rpc-service'
import userservice from '@/js/user-service'
import router from '@/router'

export default {
  name: 'RegisterPage',

  data () {
    return {
      registerUserName: '',
      registerPassword: '',
      registerDisplayName: '',
      registerEmail: '',
      registerResult: '',
      version: '',
      date: '',
    }
  },

  computed: {
    getVersionInfo() {
      rpcs.rpc('get_version_info')
        .then(response => {
          this.version = response.data['version'];
          this.date = response.data['date'];
        })
    },
  },

  methods: {
    tryRegister () {
      userservice.registerUser(this.registerUserName, this.registerPassword,
        this.registerDisplayName, this.registerEmail)
      .then(response => {
        if (response.data === 'success') { // Set a success result to show.
          this.registerResult = 'Success! Please wait while you are redirected...';
          setTimeout(function() {router.push('/login')}, 1000); // Navigate automatically to the login page after a delay
        } else { // Set a failure result to show.
          this.registerResult = response.data;
        }
      })
      .catch(error => {
          console.log('Register failed', error)
          this.registerResult = "We're sorry, it seems we're having trouble communicating with the server.  Please contact support or try again later."
      })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
