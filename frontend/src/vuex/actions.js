import logging from '../services/logging.service';
import resource from 'pilou';
const optboxes = resource('optboxes', {all: '/daemon/${resource}/'});
const printers = resource('printers', {get: '/daemon/optboxes/${optbox_id}/${resource}/'});

export default {
	getPrinters({dispatch}, optboxId) {
		printers.get({optbox_id: optboxId}).then(response => {
			dispatch('setPrinters', response.data.optbox, response.data.output.channels);
		}).catch((err) => {
			console.error(err);
			logging.error(this.$t('optboxes.get.failed'))
		});
	},
	setOptboxes({dispatch}, optboxes) {
		dispatch('setOptboxes', optboxes);
	},
	// insertOptbox({dispatch}, optbox) {
	// 	dispatch('insertOptbox', optbox);
	// },
	removeOptbox({dispatch}, optbox) {
		dispatch('removeOptbox', optbox);
	},
	setPrinters({dispatch}, optboxId, printers) {
		dispatch('setPrinters', optboxId, printers);
	},
	removePrinter({dispatch}, printer) {
		console.log('dispatch', printer)
		dispatch('removeOptbox', printer);
	}
};
