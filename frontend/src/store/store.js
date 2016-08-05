import Vue from 'vue';
import Vuex from 'vuex';
import optboxesService from '../services/optboxes';
Vue.use(Vuex);

const state = {
	count: 0,
	optboxes: [],
	printers: []
};

const mutations = {
	setOptboxes(state, optboxes) {
		state.optboxes = optboxes;
	},
	removeOptbox(state, optbox) {
		optboxesService.remove(state.optboxes, optbox);
	}
};

export default new Vuex.Store({
	state,
	mutations
});
