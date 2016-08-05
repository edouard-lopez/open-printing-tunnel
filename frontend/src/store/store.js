import Vue from 'vue';
import Vuex from 'vuex';
Vue.use(Vuex);

const state = {
	count: 0,
	optboxes: [],
	printers: []
};

const mutations = {
	setOptboxes(state, optboxes) {
		state.optboxes = optboxes;
	}
};

export default new Vuex.Store({
	state,
	mutations
});
