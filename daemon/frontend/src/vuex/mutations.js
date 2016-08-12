import sitesService from '../services/sites.service';
import printersService from '../services/printers.service';
import FileSaver from 'file-saver';


export default {
	setSites(state, sites) {
		state.sites = sites;
	},
	// todo
	// insertSite(state, site) {
	// 	state.sites.push(site);
	// },
	removeSite(state, site) {
		sitesService.remove(state.sites, site);
	},
	setPrinters(state, siteId, printers) {
		sitesService.setPrinters(state.sites, siteId, printers);
	},
	insertPrinter({dispatch}, printer) {
		dispatch('insertPrinter', printer);
	},
	removePrinter(state, printer) {
		printersService.remove(state.sites[printer.site].printers, printer);
	},
	saveFile({dispatch}, response) {
		var filename = response.headers['content-disposition'].split('=')[1];
		console.log('saving: ', filename);
		var blob = new Blob([response.data], {type: response.headers['content-type']});
		FileSaver.saveAs(blob, filename);
	},

};
