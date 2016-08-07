import optboxesService from '../services/optboxes.service';

export default {
	setOptboxes(state, optboxes) {
		state.optboxes = optboxes;
	},
	// todo
	// insertOptbox(state, optbox) {
	// 	state.optboxes.push(optbox);
	// },
	removeOptbox(state, optbox) {
		optboxesService.remove(state.optboxes, optbox);
	},
	setPrinters(state, optboxId, printers) {
		optboxesService.setPrinters(state.optboxes, optboxId, printers)
	},
	insertPrinter({dispatch}, printer) {
		dispatch('insertPrinter', printer);
	},
	removePrinter(state, printer) {
		printersService.remove(state.optboxes[printer.optbox].printers, printer);
	}
};
