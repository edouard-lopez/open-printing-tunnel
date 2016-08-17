export default {
	setSites(state, sites) {
		state.sites = sites;
	},
	clearLog(state) {
		const empty = [];
		state.log = empty;
	},
	logResponse(state, response) {
		state.log = response.results;
	}
};
