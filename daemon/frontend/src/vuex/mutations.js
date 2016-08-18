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
	},
	setPingData(state, data) {
		const siteId = Object.keys(data)[0];
		state.pings[siteId] = data[siteId];
		state.pings = {...state.pings};  // prevent vuejs reactivity caveats
	}
};
