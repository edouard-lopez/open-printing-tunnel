import optboxesService from '../services/optboxes.service';

export default {
	setOptboxes(state, optboxes) {
		for (var optbox of optboxes) {
			state.optboxes[optbox.id] = optbox;
		}
	},
	// todo
	// insertOptbox(state, optbox) {
	// 	state.optboxes.push(optbox);
	// },
	removeOptbox(state, optbox) {
		optboxesService.remove(state.optboxes, optbox);
	},
	setPrinters(state, optboxId, printers) {
		state.optboxes[optboxId].printers = printers || [];
	}
	//,
	// todo
	// removePrinter(state, printer) {
	// 	printersService.remove(state.printers, printer);
	// }
};
