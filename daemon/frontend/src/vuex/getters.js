export default {
	retrieveSites(state) {
		return state.sites;
	},
	retrieveLog(state) {
		return state.log;
	},
	retrievePings(state) {
		return state.pings;
	},
	retrieveSitePing(state, site) {
		console.log(site)
		return state.pings[site.id]
	},
	retrievePrinterPing(state, site, printer) {
		return state.pings[site.id][printer.id];
	}
};
