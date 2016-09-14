import Vue from 'vue';
import VueRouter from 'vue-router';
import VueI18n from 'vue-i18n';

import App from './components/app';
import LandingPage from './pages/index';
import SitesPage from './pages/sites/sites';
import SitePage from './pages/sites/site.component';

import auth from './services/auth.service';
import locales from './locales';

// eslint-disable-next-line no-new
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
	'/sites/': {
		component: SitesPage
	},
	'/sites/:id': {
		name: 'sites',
		component: SitePage
	}
});

auth.localStorage = localStorage;

router.beforeEach(transition => {
	if (transition.to.path === '/') {
		transition.redirect('/sites/');
	} else {
		transition.next();
	}
});

router.redirect({
	'*': '/'
});

router.start(App, '#app');
