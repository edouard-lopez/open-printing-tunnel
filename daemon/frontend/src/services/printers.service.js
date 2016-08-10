import axios from 'axios';

export default {
	localStorage: null,
	remove(printers, printerId) {
		return printers.filter(printer => {
			return printer.id !== printerId;
		});
	},
	getRequestConfig() {
		const token = this.localStorage.getItem('token');
		return {
			headers: {Authorization: `JWT ${token}`}
		};
	},
	create(printer) {
		const config = this.getRequestConfig();
		return axios.post('/api/printers/', printer, config)
			.then(response => {
				return response.data;
			});
	},
	all() {
		const config = this.getRequestConfig();
		return axios.get('/api/printers/', config)
			.then(response => {
				return response.data;
			});
	},
	get(id) {
		const config = this.getRequestConfig();
		return axios.get(`/api/printers/${id}/`, config)
			.then(response => {
				return response.data;
			});
	},
	update(printer) {
		const config = this.getRequestConfig();
		return axios.put(`/api/printers/${printer.id}/`, printer, config)
			.then(response => {
				return response.data;
			});
	},
	delete(printer) {
		const config = this.getRequestConfig();
		return axios.delete(`/api/printers/${printer.id}/`, config)
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
