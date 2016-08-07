import resource from 'pilou';
const optboxes = resource('optboxes', {all: '/daemon/${resource}/'});

export default {
	setOptboxes({dispatch}, optboxes) {
		dispatch('setOptboxes', optboxes);
	},
	insertOptbox({dispatch}, optbox) {
		dispatch('insertOptbox', optbox);
	},
	removeOptbox({dispatch}, optbox) {
		dispatch('removeOptbox', optbox);
	},
	setPrinters({dispatch}, optboxId, printers) {
		dispatch('setPrinters', optboxId, printers);
	},
	insertPrinter({dispatch}, printer) {
		dispatch('insertPrinter', printer);
	},
	// todo
	// removeOptbox({dispatch}, optbox) {
	// 	dispatch('removeOptbox', optbox);
	// }
};
