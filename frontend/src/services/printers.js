import axios from 'axios';

export default {
	localStorage: null,
	remove(printers, printerId) {
		const index = printers.findIndex(printer => printer.id === printerId);

		if (index !== -1) {
			return printers.splice(index, 1);
		}
	},
	getRequestConfig() {
		const token = this.localStorage.getItem('token');
		return {
			headers: {Authorization: `JWT ${token}`}
		};
	},
	create(printer) {
		const config = this.getRequestConfig();
		return axios.post('/daemon/printers/', printer, config)
			.then(response => {
				return response.data;
			});
	},
	all() {
		const config = this.getRequestConfig();
		return axios.get('/daemon/printers/', config)
			.then(response => {
				return response.data;
			});
	},
	get(id) {
		const config = this.getRequestConfig();
		return axios.get(`/daemon/printers/${id}/`, config)
			.then(response => {
				return response.data;
			});
	},
	update(printer) {
		const config = this.getRequestConfig();
		return axios.put(`/daemon/printers/${printer.id}/`, printer, config)
			.then(response => {
				return response.data;
			});
	},
	delete(printer) {
		const config = this.getRequestConfig();
		return axios.delete(`/daemon/printers/${printer.id}/`, config)
			.then(response => {
				return response.data;
			});
	},
	parseLine(line) {
		if (line) {
			const fields = line.split('\t');

			return {
				DESC: fields[0],
				PRINTER: fields[1],
				PORT: fields[2] || null
			};
		}
	},
	parsePrinters(clipboard) {
		return clipboard.split('\n')
			.filter(line => {
				return line;
			})
			.map(line => {
				return this.parseLine(line);
			});
	}
};
