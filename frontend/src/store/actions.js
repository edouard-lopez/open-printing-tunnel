export default {
	setOptboxes({dispatch}, optboxes) {
		dispatch('setOptboxes', optboxes);
	},
	removeOptbox({dispatch}, optbox) {
		dispatch('removeOptbox', optbox);
	}
};
