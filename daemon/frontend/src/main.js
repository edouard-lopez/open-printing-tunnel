import Vue from 'vue';
import VueRouter from 'vue-router';

import App from './components/app';
import store from './vuex/store';
import SitesPage from './pages/sites/sites';

Vue.config.debug = true;

Vue.use(VueRouter);
// eslint-disable-next-line no-new
const router = new VueRouter()
  .map({ '/': { component: SitesPage } })
  .redirect({ '*': '/' })
  .start(App, '#app');

// eslint-disable-next-line no-new
new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
});
