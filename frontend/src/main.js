import Vue from 'vue';
import VueRouter from 'vue-router';
import VueI18n from 'vue-i18n';

import App from './components/app';
import LandingPage from './pages/index';
import LoginPage from './pages/login';
import ContainersPage from './pages/containers/containers';
import ContainerPage from './pages/containers/container.details';
import OptboxesPage from './pages/optboxes/optboxes';
import RegisterPage from './pages/register';
import SettingsPage from './pages/settings';

import './services/array.polyfill';
import auth from './services/auth.service';
import locales from './locales';

new Vue({
	el: '#app',
	render: h => h(App)
});

Vue.use(VueI18n);
const browserLanguage = (navigator.language || navigator.browserLanguage).split('-')[0];
const lang = browserLanguage in locales ? browserLanguage : 'en';
Vue.config.lang = lang;
Object.keys(locales).forEach(lang => {
	Vue.locale(lang, locales[lang]);
});

Vue.use(VueRouter);
const router = new VueRouter();

router.map({
	'/': {
		component: LandingPage
	},
	'/login/': {
		component: LoginPage
	},
	'/register/': {
		component: RegisterPage
	},
	'/settings/': {
		component: SettingsPage,
		authRequired: true
	},
	'/containers/': {
		component: ContainersPage,
		authRequired: true
	},
	'/containers/:id': {
		component: ContainerPage,
		authRequired: true
	},
	'/optboxes/': {
		component: OptboxesPage,
		authRequired: true
	}
});

auth.localStorage = localStorage;

router.beforeEach(transition => {
	auth.checkAuth()
		.then(() => {
			if (transition.to.path === '/') {
				transition.redirect('/containers/');
			} else {
				transition.next();
			}
		})
		.catch(() => {
			if (transition.to.authRequired) {
				transition.redirect('/login/');
			} else {
				transition.next();
			}
		});
});

router.redirect({
	'*': '/'
});

router.start(App, '#app');
