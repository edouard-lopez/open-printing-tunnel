import sitesService from '../services/sites.service';
import printersService from '../services/printers.service';

export default {
	setSites(state, sites) {
		state.sites = sites;
	},
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
	}
};
