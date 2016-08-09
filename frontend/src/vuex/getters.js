export default {
	retrieveSites(state) {
		return state.sites;
	},
	retrievePrinters(state, siteId) {
		return state.sites[siteId].printer;
	}
};
