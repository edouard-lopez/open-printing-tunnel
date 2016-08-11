import http from 'services/http.service';
import logging from '../services/logging.service';

const sites = http('sites', localStorage);
const printers = http('printers', localStorage);

export default {
	getSites({dispatch}) {
		sites.all().then((response) => {
			dispatch('setSites', response.data.results);
		}).catch(() => {
			this.no_site_message = 'there is no site';
			logging.error(this.$t('sites.get.failed'))
		});
	},
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
