import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';

Vue.use(Router);

export const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
  ]
});

// router.beforeEach((to, from, next) => {
//   const publicPages = ['/login', '/register','/home'];
//   const adminPages = ['/admin']
//   const authRequired = !publicPages.includes(to.path);
//   const adminRequired = adminPages.includes(to.path);
//   const loggedIn = localStorage.getItem('user');
//   const currentUser = JSON.parse(loggedIn);
//   // trying to access a restricted page + not logged in
//   // redirect to login page
//   if (authRequired && !loggedIn) {
//     next('/login');
//   } else {
//     next();
//   }

//   if (adminRequired && !currentUser.roles.includes('Admin')) {
//     next('/');
//   } else {
//     next();
//   }
// });
