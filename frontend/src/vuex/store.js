import Vue from 'vue';
import Vuex from 'vuex';
import mutations from './mutations';
import createLogger from '../middlewares/logger'

Vue.use(Vuex);
Vue.config.debug = true

const debug = process.env.NODE_ENV !== 'production'

const state = {
	count: 0,
	optboxes: {},
};


export default new Vuex.Store({
	state,
	mutations,
	strict: debug,
	middlewares: debug ? [createLogger()] : []
});
