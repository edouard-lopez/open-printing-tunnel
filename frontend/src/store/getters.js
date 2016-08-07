export default {
	retrieveOptboxes(state) {
		return state.optboxes;
	},
	retrievePrinters(state, optboxId) {
		return state.optboxes[optboxId].printer ;
	},
};
