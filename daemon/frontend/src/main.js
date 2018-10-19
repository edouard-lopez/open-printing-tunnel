import Vue from 'vue';
import VueRouter from 'vue-router';

import App from './components/app';
import SitesPage from './pages/sites/sites';

Vue.use(VueRouter);
const router = new VueRouter()
	.map({'/': {component: SitesPage}})
	.redirect({'*': '/'})
	.start(App, '#app');

new Vue({
	el: '#app',
	router,
	render: h => h(App)
});

