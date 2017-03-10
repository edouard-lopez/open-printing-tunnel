import resource from 'pilou';
import http from '../services/http.service';
import logging from '../services/logging.service';

const printers = resource('printers', {get: '/api/sites/${site_id}/${resource}/'});
const DaemonService = http('daemons', localStorage);

export default {
	getPrinters({dispatch}, siteId) {
		printers.get({site_id: siteId}).then(response => {
			dispatch('setPrinters', response.data.site, response.data.output.channels);
		}).catch(err => {
			console.error(err);
			logging.error(this.$t('printers.get.failed'));
		});
	},
	setSites({dispatch}, sites) {
		dispatch('setSites', sites);
	},
	removeSite({dispatch}, site) {
		dispatch('removeSite', site);
	},
	setPrinters({dispatch}, siteId, printers) {
		dispatch('setPrinters', siteId, printers);
	},
	removePrinter({dispatch}, printer) {
		dispatch('removeSite', printer);
	},
	fetchDaemon({dispatch}, id) {
		DaemonService.get({id}).then(response => {
			dispatch('SET_DAEMON', response.data);
		});
	}
};
