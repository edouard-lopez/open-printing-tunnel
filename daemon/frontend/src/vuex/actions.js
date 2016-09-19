import http from 'services/http.service'; // eslint-disable-line import/no-extraneous-dependencies
import logging from 'services/logging.service'; // eslint-disable-line import/no-extraneous-dependencies
import resource from 'pilou';
import FileSaver from 'file-saver';
import scannerFilter from '../components/scan.filter.js';

const sites = http('sites', localStorage);
const scripts = http('scripts', localStorage);
const printers = http('printers', localStorage);
const networks = http('networks', localStorage);
const scan = http('scan', localStorage);

export default {
	addPrinter({dispatch}, printer) {
		return printers.create(printer).then(response => {
			logging.success('Ajout de l\'imprimante réussi.');
			return response;
		}).catch(err => {
			console.log('failed to add printer', err);
			logging.error('Échec de l\'ajout de l\'imprimante !');
		});
	},
	getSites({dispatch}) {
		sites.all().then(response => {
			dispatch('setSites', response.data.results);
		}).catch(() => {
			logging.error('Échec de la récupération des sites !');
		});
	},
	getPrinterScript({dispatch}, site, printer) {
		return scripts.get(
			{site: site.id, id: printer.id},
			{url: '/api/${resource}/${site}/printers/${id}/'})
			.then(response => {
				logging.success('Génération du script réussi.');
				return response;
			})
			.catch(err => {
				console.error(err);
				logging.error('Échec de la génération du script !');
			});
	},
	getSiteScript({dispatch}, site) {
		return scripts.get({id: site.id}).then(response => {
			logging.success('Génération du script réussi.');
			return response;
		}).catch(err => {
			console.error('deletion failed', err);
			logging.error('Échec de la génération du script !');
		});
	},
	saveFile({dispatch}, response) {
		const filename = response.headers['content-disposition'].split('=')[1];
		console.info('saving: ', filename);
		const blob = new Blob([response.data], {type: response.headers['content-type']});
		FileSaver.saveAs(blob, filename);
	},
	setSites({dispatch}, sites) {
		dispatch('setSites', sites);
	},
	setPrinters({dispatch}, siteId, printers) {
		dispatch('setPrinters', siteId, printers);
	},
	deleteSite({dispatch}, site) {
		return sites.delete(site).then(() => {
			logging.success('Suppression du site réussie.');
		}).catch(() => {
			logging.error('Impossible de supprimer ce site pour l\'instant. Retentez dans quelques instants ou contacter un administrateur');
		});
	},
	deletePrinter({dispatch}, site, printer) {
		const printers = resource('printers', {delete: '/api/sites/${site}/${resource}/${id}/'});

		return printers.delete({site: site.id, id: printer.id}).then(() => {
			logging.success('Suppression de l\'imprimante réussie.');
		}).catch(err => {
			console.log('deletion failed', err);
			logging.error('Échec de la suppression !');
		});
	},
	scanSite({dispatch}, site) {
		return scan.get({site: site.hostname}, {url: '/api/${resource}/${site}/'})
			.then(response => {
				const printers = scannerFilter.printers(response.data);
				response.results = scannerFilter.clipboard(printers);
				dispatch('logResponse', response);
				const found = printers.length;
				if (found === 0) {
					logging.warning('Scan du réseau terminé : aucune imprimante trouvée.');
				} else {
					logging.success('Scan du réseau terminé : ' + found + ' imprimantes trouvées.');
				}
				return response;
			})
			.catch(err => {
				console.error(err);
				logging.error('Échec du scan du réseau !');
			});
	},
	siteStatus({dispatch}, site) {
		site.action = 'status';
		sites.update(site).then(response => {
			dispatch('logResponse', response.data);
		});
	},
	siteStart({dispatch}, site) {
		site.action = 'start';
		sites.update(site).then(response => {
			dispatch('logResponse', response.data);
			logging.success('Démarrage réussi.');
		}).catch(() => {
			logging.error('Échec du démarrage.');
		});
	},
	siteStop({dispatch}, site) {
		site.action = 'stop';
		sites.update(site).then(response => {
			dispatch('logResponse', response.data);
			logging.success('Arrêt réussi.');
		}).catch(() => {
			logging.error('Échec de l\'arrêt.');
		});
	},
	siteRestart({dispatch}, site) {
		site.action = 'restart';
		sites.update(site).then(response => {
			dispatch('logResponse', response.data);
			logging.success('Redémarrage réussi.');
		}).catch(() => {
			logging.error('Échec du redémarrage.');
		});
	},
	clearLog({dispatch}) {
		dispatch('clearLog');
	},
	logResponse({dispatch}, response) {
		if (!Array.isArray(response.results)) {
			response.results = [response.results];
		}
		dispatch('logResponse', response);
	},
	probeNetwork({dispatch}) {
		function sendProbe() {
			networks.all().then(response => {
				dispatch('setNetworksData', response.data);
			}).catch(err => {
				console.error('Échec de la récupération des networks.', err);
			});
		}

		sendProbe();
		setInterval(() => sendProbe(), 15 * 1000);
	}
};
