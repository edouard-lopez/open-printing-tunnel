function storageMock() {
	const storage = {};

	return {
		setItem: (key, value) => {
			storage[key] = value || '';
		},
		getItem: key => {
			return storage[key] || null;
		},
		removeItem: key => {
			delete storage[key];
		},
		get length() {
			return Object.keys(storage).length;
		},
		key: i => {
			const keys = Object.keys(storage);
			return keys[i] || null;
		}
	};
}
export { storageMock };

const sitesGetAll = {
	results: [
		{
			id: 'bordeaux',
			hostname: '10.0.0.1'
		},
		{
			id: 'marmande',
			hostname: '10.0.0.2'
		},
		{
			id: 'cestas',
			hostname: '10.0.0.3'
		}
	]
};
export { sitesGetAll };

const siteGetOne = JSON.parse(JSON.stringify(sitesGetAll.results[0]));
export { siteGetOne };

const printersGetAll = {
	data: [
		{
			id: 0,
			hostname: '1.2.3.4',
			description: 'salle 1'
		},
		{
			id: 4,
			hostname: '1.2.3.5',
			description: 'salle 2'
		},
		{
			id: 3,
			hostname: '1.2.3.6',
			description: 'salle 3'
		}
	]
};
export { printersGetAll };

const printerGetOne = JSON.parse(JSON.stringify(printersGetAll.data[0]));
export { printerGetOne };
