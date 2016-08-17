import http from 'services/http.service';
import logging from 'services/logging.service';
import resource from 'pilou';
import FileSaver from 'file-saver';

const sites = http('sites', localStorage);
const scripts = http('scripts', localStorage);

export default {
	getSites({dispatch}) {
		sites.all().then(response => {
			dispatch('setSites', response.data.results);
		}).catch(() => {
			logging.error('Échec de la récupération des sites !');
		});
	},
	getPrinterScript({dispatch}, site, printer) {
		return scripts.get(
			{site_id: site.id, printer_id: printer.id},
			{url: '/api/${resource}/${site_id}/printers/${printer_id}/'})
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
		const printers = resource('printers', {delete: '/api/sites/${site_id}/${resource}/${printer_id}/'});

		return printers.delete({site_id: site.id, printer_id: printer.id}).then(() => {
			logging.success('Suppression de l\'imprimante réussie.');
		}).catch(err => {
			console.log('deletion failed', err);
			logging.error('Échec de la suppression !');
		});
	},
	siteStatus({dispatch}, site) {
		site['action'] = 'status';
		sites.update(site).then(response => {
			dispatch('logResponse', response.data);
		});
	},
	siteStart({dispatch}, site) {
		site['action'] = 'start';
		sites.update(site).then(response => {
			dispatch('logResponse', response.data);
			logging.success(this.$t('Démarrage réussi.'));
		}).catch(() => {
			logging.error(this.$t('Échec du démarrage.'))
		});
	},
	siteStop({dispatch}, site) {
		site['action'] = 'stop';
		sites.update(site).then(response => {
			dispatch('logResponse', response.data);
			logging.success(this.$t('Arrêt réussi.'));
		}).catch(() => {
			logging.error(this.$t('Échec de l\'arrêt.'))
		});
	},
	siteRestart({dispatch}, site) {
		site['action'] = 'restart';
		sites.update(site).then(response => {
			dispatch('logResponse', response.data);
			logging.success(this.$t('Redémarrage réussi.'));
		}).catch(() => {
			logging.error(this.$t('Échec du redémarrage.'))
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
	}
};
