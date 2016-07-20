import Vue from 'vue';
import VueRouter from 'vue-router';
import VueI18n from 'vue-i18n';

import App from './app';
import LandingPage from './pages/index';
import LoginPage from './pages/login';
import ContainersPage from './pages/containers';
import ContainerPage from './pages/container';
import ContainerCreatePage from './pages/container.create';
import PrintersPage from './pages/printers';
import PrintersAddPage from './pages/printers.add';
import PrinterPage from './pages/printer';
import RegisterPage from './pages/register';
import SettingsPage from './pages/settings';
import auth from './services/auth';
import locales from './locales';

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
	'/containers/create/': {
		component: ContainerCreatePage,
		authRequired: true
	},
	'/printers/': {
		component: PrintersPage,
		authRequired: true
	},
	'/containers/add/': {
		component: PrintersAddPage,
		authRequired: true
	},
	'/printers/:id': {
		component: PrinterPage,
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

router.start(App, 'app');