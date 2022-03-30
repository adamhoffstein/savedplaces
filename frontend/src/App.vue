<template>
  <v-app id="app">
    <v-app-bar app color="primary" flat dark>
      <v-container fluid class="py-0 fill-height">
        <v-btn v-if="currentUser" text to="/">
          <v-icon> mdi-home </v-icon>
        </v-btn>
        <v-spacer></v-spacer>
        <v-btn v-if="currentUser" text @click="logOut"> Sign Out </v-btn>
        <v-btn v-if="!currentUser" text to="/register"> Register </v-btn>
        <v-btn v-if="!currentUser" text to="/login"> Login </v-btn>
      </v-container>
    </v-app-bar>
    <v-main class="grey lighten-3">
      <v-container fluid>
        <v-row>
          <v-col>
            <v-sheet min-height="70vh" rounded="lg" color="grey lighten-3">
              <router-view :key="$route.fullPath" />
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>
<script>
export default {
  name: 'App',
  data () {
    return {
      drawer: false,
    };
  },
  components: {
  },
  computed: {
    links(){
      if(this.currentUser){
        return [
          {path:'/', name:'Home'},
        ]
      }
      else{
        return []
        }
    },
    currentUser() {
      return {username: 'bob', roles: []};
    },
    showAdminBoard() {
      if (this.currentUser && this.currentUser.roles.includes('Admin')) {
        return true;
      }
      return false;
    }
  },
  methods: {
    logOut() {
      this.$store.dispatch('auth/logout');
      this.$router.push('/login');
    }
  }
};
</script>
