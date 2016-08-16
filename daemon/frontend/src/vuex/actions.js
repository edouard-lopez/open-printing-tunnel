import http from 'services/http.service';
import logging from '../services/logging.service';

const sites = http('sites', localStorage);
const printers = http('printers', localStorage);
const scripts = http('scripts', localStorage);
import resource from 'pilou';

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
	deleteSite({dispatch}, site) {
		return sites.delete(site).then(() => {
			dispatch('getSites');
			logging.success('Suppression du site réussie.');
		}).catch(() => {
			logging.error('Impossible de supprimer ce site pour l\'instant. Retentez dans quelques instants ou contacter un administrateur')
		});
	},
	deletePrinter({dispatch}, site, printer) {
		const printers = resource('printers', {delete: '/api/sites/${site_id}/${resource}/${printer_id}/'});

		return printers.delete({site_id: site.id, printer_id: printer.id}).then((response) => {
			dispatch('getSites');
			logging.success('Suppression de l\'imprimante réussie.');
		}).catch((err) => {
			console.log('deletion failed', err);
			logging.error('Échec de la suppression !');
		});
	removePrinter({dispatch}, printer) {
		dispatch('removeSite', printer);
	}
};
