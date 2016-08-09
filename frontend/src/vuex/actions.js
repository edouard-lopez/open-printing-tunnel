import logging from '../services/logging.service';
import resource from 'pilou';
const sites = resource('sites', {all: '/daemon/${resource}/'});
const printers = resource('printers', {get: '/daemon/sites/${site_id}/${resource}/'});

export default {
	getPrinters({dispatch}, siteId) {
		printers.get({site_id: siteId}).then(response => {
			dispatch('setPrinters', response.data.site, response.data.output.channels);
		}).catch((err) => {
			console.error(err);
			logging.error(this.$t('printers.get.failed'))
		});
	},
	setSites({dispatch}, sites) {
		dispatch('setSites', sites);
	},
	// insertSite({dispatch}, site) {
	// 	dispatch('insertSite', site);
	// },
	removeSite({dispatch}, site) {
		dispatch('removeSite', site);
	},
	setPrinters({dispatch}, siteId, printers) {
		dispatch('setPrinters', siteId, printers);
	},
	removePrinter({dispatch}, printer) {
		console.log('dispatch', printer)
		dispatch('removeSite', printer);
	}
};
