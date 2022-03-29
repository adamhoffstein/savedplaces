<template>
  <v-app id="app">
    <v-navigation-drawer
      v-if="currentUser"
      v-model="drawer"
      app
      flat
      color="toolbar"
      dark
    >
    <v-row justify="center"
    class="pt-10 pb-10"
    >
      <v-avatar
      color="primary"
      size="100"
      >
        <img
        src="https://i2.wp.com/www.cycat.io/wp-content/uploads/2018/10/Default-user-picture.jpg"
        >

      </v-avatar>
    </v-row>
      <v-divider></v-divider>
      <v-list
        dense
        nav
      >
        <v-list-item
          to="/browse"
          link
        >
          <v-list-item-icon>
            <v-icon>mdi-folder</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            Browse
          </v-list-item-content>
        </v-list-item>
        <v-list-item
          to="/notebooks"
          link
        >
          <v-list-item-icon>
            <v-icon>mdi-chart-areaspline</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            Notebooks
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item
          to="/admin"
          v-if="showAdminBoard"
          link
        >
          <v-list-item-icon>
            <v-icon>mdi-shield</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            Admin Panel
          </v-list-item-content>
        </v-list-item>
        <v-list-item
          to="/settings"
          link
        >
          <v-list-item-icon>
            <v-icon>mdi-cog</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            Settings
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      app
      color="primary"
      flat
      dark
    >
      <v-container fluid class="py-0 fill-height">
        <v-app-bar-nav-icon
        @click="drawer = !drawer"
        v-if="currentUser"
        >
      </v-app-bar-nav-icon>
      <v-btn v-if="currentUser"
        text
        to="/"
        >
        <v-icon>
        mdi-home
        </v-icon>
      </v-btn>
      <v-spacer></v-spacer>
        <v-btn v-if="currentUser"
          text
          @click="logOut"
          >
          Sign Out
        </v-btn>
        <v-btn v-if="!currentUser"
          text
          to="/register"
          >
          Register
        </v-btn>
        <v-btn v-if="!currentUser"
          text
          to="/login"
          >
          Login
        </v-btn>
      </v-container>
    </v-app-bar>
    <v-main class="grey lighten-3">
      <v-container fluid>
        <v-row>
          <v-col>
            <v-sheet
              min-height="70vh"
              rounded="lg"
              color="grey lighten-3"
            >
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
