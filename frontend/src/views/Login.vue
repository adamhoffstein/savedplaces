<template>
  <v-container style="maxWidth:700px"
  >
    <v-layout flex align-center justify-center>
      <v-flex elevation-2>
        <v-toolbar class="pt-5 primary">
          <v-toolbar-items>
          <v-toolbar-title class="white--text">Login</v-toolbar-title>
          </v-toolbar-items>
        </v-toolbar>
        <v-card
        class="mx-auto"
        :loading="loadingLogin"
        >
          <v-card-text class="pt-4">
            <div>
              <form @submit.prevent="handleLogin">
                <v-text-field
                  v-model="username"
                  :error-messages="usernameErrors"
                  label="Username"
                  required
                  @input="$v.username.$touch()"
                  @blur="$v.username.$touch()"
                ></v-text-field>
                <v-text-field
                  v-model="password"
                  :type="show1 ? 'text' : 'password'"
                  :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                  :error-messages="passwordErrors"
                  label="Password"
                  required
                  @input="$v.password.$touch()"
                  @blur="$v.password.$touch()"
                  @click:append="show1 = !show1"
                ></v-text-field>
                <v-alert
                  dense
                  v-if="showLoginError"
                  outlined
                  type="error"
                >
                  {{loginErrors}}
                </v-alert>
                <v-layout justify-space-between>
                  <v-btn
                    class="mr-4"
                    @click="submit"
                  >
                    Login
                  </v-btn>
                  <a href="">Forgot your Password</a>
                  <router-link to="/register">Don't have an account?</router-link>
                </v-layout>
              </form>
              <v-layout justify-center>
                <google-login>
                </google-login>
              </v-layout>
            </div>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import { validationMixin } from 'vuelidate'
  import { required } from 'vuelidate/lib/validators'
  import User from '../models/user';
  import GoogleLogin from "../components/GoogleLogin";


  export default {
    name: 'Login',
    components: {
      GoogleLogin
    },
    mixins: [validationMixin],

    validations: {
      username: { required },
      password: { required },
    },

    data: () => ({
      user: new User('', ''),
      username: '',
      password: '',
      loginErrors: 'Incorrect username or password',
      loadingLogin: false,
      showLoginError: false,
      show1: false,
    }),

    computed: {
      usernameErrors () {
        const errors = []
        if (!this.$v.username.$dirty) return errors
        !this.$v.username.required && errors.push('Name is required.')
        return errors
      },
      passwordErrors () {
        const errors = []
        if (!this.$v.password.$dirty) return errors
        !this.$v.password.required && errors.push('Password is required')
        return errors
      },
    },

    methods: {
      submit () {
        this.$v.$touch()
        this.handleLogin()
      },
      clear () {
        this.$v.$reset()
        this.username = ''
        this.password = ''
      },
      handleLogin() {
        this.loading = true;
        this.user.username = this.username;
        this.user.password = this.password;
        if (this.user.username && this.user.password) {
          this.loadingLogin = true;
          this.$store.dispatch('auth/login', this.user).then(
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
    },
  }
</script>
