export default {
	setSites(state, sites) {
		state.sites = sites;
	},
	clearLog(state) {
		let empty = [];
		state.log = empty;
	},
	logResponse(state, response) {
		state.log = response.results;
	}
};
