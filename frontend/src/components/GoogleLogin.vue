<template>
  <v-btn primary v-google-signin-button="clientId">Login with Google</v-btn>
</template>

<script>
import GoogleSignInButton from 'vue-google-signin-button-directive'
export default {
  directives: {
    GoogleSignInButton
  },
  data: () => ({
    clientId: '.apps.googleusercontent.com'
  }),
  methods: {
    OnGoogleAuthSuccess (idToken) {
      console.log(idToken)
      this.handleLogin(idToken)

    },
    OnGoogleAuthFail (error) {
      console.log(error)
    },
    handleLogin(idToken) {
      this.loading = true;
      this.loadingLogin = true;
      this.$store.dispatch('auth/logingoogle', idToken).then(
        () => {
          this.$router.push('/');
        },
        error => {
          this.loadingLogin = false;
          this.showLoginError = true
          this.message =
            (error.response && error.response.data) ||
            error.message ||
            error.toString();
        }
      );
    }
  }
}
</script>

<style type="text/css">

</style>
