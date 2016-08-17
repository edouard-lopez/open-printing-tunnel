export default {
	retrieveSites(state) {
		return state.sites;
	},
	retrieveLog(state) {
		console.log('getter: log')
		return state.log;
	}
};
