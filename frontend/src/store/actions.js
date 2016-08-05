export default {
	incrementCounter({dispatch, state}) {
		dispatch('INCREMENT', 1)
	},
	setOptboxes({dispatch, state}, optboxes) {
		dispatch('setOptboxes', optboxes)
	},
	removeOptbox({dispatch, state}, optbox_id) {
		dispatch('removeOptbox', optbox_id)
	},
}
