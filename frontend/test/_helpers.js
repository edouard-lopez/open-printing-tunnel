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
export {storageMock};

const containersGetAll = {
	count: 2,
	next: null,
	previous: null,
	results: [
		{
			id: '049fed91-6880-4c08-8cb2-21e8579d4543',
			description: '您的瀏覽器需要安裝Flash插件 ',
			company: '0d8dbbf3-73f4-49ab-a550-22c1fca93439',
			container_id: 'a5775b3cf95c465d5abcee59934c087cad9ca3d20bee266c44576b7b3d06ac1c',
			infos: {
				id: 'a5775b3cf95c465d5abcee59934c087cad9ca3d20bee266c44576b7b3d06ac1c',
				status: 'running',
				name: '/mast__e45b0231-251f-401d-b379-eb5875fc343b'
			}
		},
		{
			id: '0d8dbbf3-73f4-49ab-a550-22c1fca93439',
			description: '為了更好瀏覽多媒體內容',
			company: '049fed91-6880-4c08-8cb2-21e8579d4543',
			container_id: 'a5775b3cf95c465d5abcee59934c087cad9ca3d20bee266c44576b7b3d06ac1c',
			infos: {
				id: 'a5775b3cf95c465d5abcee59934c087cad9ca3d20bee266c44576b7b3d06ac1c',
				status: 'running',
				name: '/mast__e45b0231-251f-401d-b379-eb5875fc343b'
			}
		}
	]
};
export {containersGetAll};

const containersGetOne = JSON.parse(JSON.stringify(containersGetAll.results[0]));
export {containersGetOne};

const optboxesGetAll = {
	results: [
		{
			name: 'Bordeaux',
			hostname: 'bordeaux.opt'
		},
		{
			name: 'Marmande',
			hostname: 'marmande.opt'
		},
		{
			name: 'Cestas',
			hostname: 'cestas.opt'
		}
	]
};
export {optboxesGetAll};

const optboxGetOne = JSON.parse(JSON.stringify(optboxesGetAll.results[0]));
export {optboxGetOne};


const printersGetAll = {
	data: [
		{
			name: 'imprimante 1',
			hostname: '1.2.3.4',
			description: 'salle 1',
		},
		{
			name: 'imprimante 2',
			hostname: '1.2.3.5',
			description: 'salle 2',
		},
		{
			name: 'imprimante 3',
			hostname: '1.2.3.6',
			description: 'salle 3',
		}
	]
};
export {printersGetAll};

const printerGetOne = JSON.parse(JSON.stringify(printersGetAll.data[0]));
export {printerGetOne};
