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

const optBoxesGetAll = {
	count: 4,
	next: null,
	previous: null,
	results: [
		{
			id: '049fed91-6880-4c08-8cb2-21e8579d4543',
			name: 'Cenon',
			company: '049fed91-6880-4c08-8cb2-21e8579d4543',
			address: 'bordeaux.opt'
		},
		{
			id: '0d8dbbf3-73f4-49ab-a550-22c1fca93439',
			name: 'Marmande',
			company: '049fed91-6880-4c08-8cb2-21e8579d4543',
			address: 'marmande.opt'
		},
		{
			id: '92e66964-cdc3-4186-a121-603a11980763',
			name: 'Cestas',
			company: '049fed91-6880-4c08-8cb2-21e8579d4543',
			address: 'cestas.opt'
		}
	]
};
export {optBoxesGetAll};

const optBoxGetOne = JSON.parse(JSON.stringify(optBoxesGetAll.results[0]));
export {optBoxGetOne};


const optboxesGetAll = {
	count: 3,
	next: null,
	previous: null,
	results: [
		{
			id: 1,
			location: 'salle de réunion (Cenon)',
			name: '049fed91-6880-4c08-8cb2-21e8579d4543',
			address: '10.1.4.1'
		},
		{
			id: 2,
			location: 'salle de réunion (Marmande)',
			name: '0d8dbbf3-73f4-49ab-a550-22c1fca93439',
			address: '10.1.4.2'
		},
		{
			id: 3,
			location: 'salle de réunion (Cestas)',
			name: '92e66964-cdc3-4186-a121-603a11980763',
			address: '10.1.4.1'
		}
	]
};
export {optboxesGetAll};

const optboxGetOne = JSON.parse(JSON.stringify(optboxesGetAll.results[0]));
export {optboxGetOne};
