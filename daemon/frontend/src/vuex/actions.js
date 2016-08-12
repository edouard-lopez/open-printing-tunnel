import http from 'services/http.service';
import logging from '../services/logging.service';

const sites = http('sites', localStorage);
const printers = http('printers', localStorage);
const scripts = http('scripts', localStorage);

export default {
	getSites({dispatch}) {
		sites.all().then((response) => {
			dispatch('setSites', response.data.results);
		}).catch(() => {
			this.no_site_message = 'there is no site';
			logging.error('Échec de la récupération des sites.');
		});
	},
	getPrinters({dispatch}, siteId) {
		printers.get({site_id: siteId}).then(response => {
			dispatch('setPrinters', response.data.site, response.data.results.channels);
		}).catch(err => {
			console.error(err);
			logging.error('Échec de la récupération des imprimantes.');
		});
	},
	getPrinterScript({dispatch}, siteId, printerId)  {
		scripts.get(
			{site_id: siteId, printer_id: printerId},
			{url: '/api/${resource}/${site_id}/printers/${printer_id}/'})
			.then(response => {
				logging.success('Génération du script réussi.');
				dispatch('saveFile', response);
			})
			.catch(err => {
				console.error(err);
				logging.error('Échec de la génération du script.');
			});
	},
	getSiteScript({dispatch}, site_id) {
		scripts.get({id: site_id}).then((response) => {
			dispatch('saveFile', response);
			logging.success('Génération du script réussi.');
		}).catch((err) => {
			console.log('deletion failed', err);
			logging.error('Échec de la génération du script.');
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
	}
};
