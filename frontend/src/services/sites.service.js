export default {
	localStorage: null,
	getIndex(sites, siteId) {
		return sites.findIndex(current => current.id === siteId);
	},
	setPrinters(sites, siteId, printers) {
		const index = this.getIndex(sites, siteId);
		console.log('setPrinters', siteId, index, sites[index], printers);
		sites[index] = {...sites[index], printers: printers};
	},
	remove(sites, site) {
		const index = sites.findIndex(current => current.id === site.id);
		if (index !== -1) {
			return sites.splice(index, 1);
		}
	}
};
