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
	setNetworksData(state, data) {
		state.networks = data;
		state.networks = {...state.networks};  // prevent vuejs reactivity caveats
	},
	setScanClipboard(state, site) {
		state.scans[site.id] = site.scan;
		state.scans = {...state.scans};  // prevent vuejs reactivity caveats
	},
	setSiteConfig(state, {site, config}) {
		const siteIndex = state.sites.findIndex(item => item.id === site.id);

		if (siteIndex !== -1) {
			state.sites[siteIndex].config = config;
		}
	}
};
