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
		return state.pings[site.id];
	},
	retrievePrinterPing(state, printer) {
		return state.pings[printer.site][printer.hostname];
	}
};
