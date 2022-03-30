import Vue from 'vue';
import App from './App.vue';
import { router } from './router';
import Axios from 'axios'
import axios from 'axios';
// import store from './store';
import VeeValidate from 'vee-validate';
import vuetify from './plugins/vuetify';
// import createAuthRefreshInterceptor from 'axios-auth-refresh';
import VueAxios from 'vue-axios'
import * as VueGoogleMaps from 'vue2-google-maps'
import ApiService from "./services/api.service";

Vue.config.productionTip = false;

Vue.prototype.$http = Axios;

// let user = JSON.parse(localStorage.getItem('user'));

// const refreshAuthLogic = failedRequest => axios.post(API_URL + 'auth/refresh', {'refresh_token': user.refresh_token}).then(tokenRefreshResponse => {
//     localStorage.setItem('user', JSON.stringify(tokenRefreshResponse.data));
//     console.log('REFRESH RESPONSE: ' ,tokenRefreshResponse)
//     failedRequest.response.config.headers['Authorization'] = 'Bearer ' + tokenRefreshResponse.data.access_token;
//     console.log('RETRYING REQUEST')
//     return Promise.resolve();
// });

// createAuthRefreshInterceptor(axios, refreshAuthLogic);


Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyDHA6k6vxs0CpJCXNHo0C9I_1Svd_aifMY',
    libraries: 'places', // This is required if you use the Autocomplete plugin
    // OR: libraries: 'places,drawing'
    // OR: libraries: 'places,drawing,visualization'
    // (as you require)

    //// If you want to set the version, you can do so:
    // v: '3.26',
  },

  //// If you intend to programmatically custom event listener code
  //// (e.g. `this.$refs.gmap.$on('zoom_changed', someFunc)`)
  //// instead of going through Vue templates (e.g. `<GmapMap @zoom_changed="someFunc">`)
  //// you might need to turn this on.
  // autobindAllEvents: false,

  //// If you want to manually install components, e.g.
  //// import {GmapMarker} from 'vue2-google-maps/src/components/marker'
  //// Vue.component('GmapMarker', GmapMarker)
  //// then set installComponents to 'false'.
  //// If you want to automatically install all the components this property must be set to 'true':
  installComponents: true
})


Vue.config.productionTip = false;

Vue.use(VeeValidate);

Vue.use(VueAxios, axios);

ApiService.init();

new Vue({
  router,
  // store,
  vuetify,
  render: h => h(App)
}).$mount('#app');
