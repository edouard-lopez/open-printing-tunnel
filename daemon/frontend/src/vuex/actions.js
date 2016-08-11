import resource from 'pilou';
import logging from '../services/logging.service';
const printers = resource('printers', {get: '/api/sites/${site_id}/${resource}/'});

export default {
	getPrinters({dispatch}, siteId) {
		printers.get({site_id: siteId}).then(response => {
			dispatch('setPrinters', response.data.site, response.data.results.channels);
		}).catch(err => {
			console.error(err);
			logging.error(this.$t('printers.get.failed'));
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
		dispatch('removeSite', printer);
	}
};
