import Vue from 'vue';
import VueRouter from 'vue-router';
import VueI18n from 'vue-i18n';

import App from './components/app';
import SitesPage from './pages/sites/sites';

Vue.use(VueRouter);
const router = new VueRouter()
	.map({'/': {component: SitesPage}})
	.redirect({'*': '/'})
	.start(App, '#app');
import locales from './locales';

new Vue({
	el: '#app',
	router,
	render: h => h(App)
});

Vue.use(VueI18n);
const browserLanguage = (navigator.language || navigator.browserLanguage).split('-')[0];
const lang = browserLanguage in locales ? browserLanguage : 'en';
Vue.config.lang = lang;
Object.keys(locales).forEach(lang => {
	Vue.locale(lang, locales[lang]);
});
