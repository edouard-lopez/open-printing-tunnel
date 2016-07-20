import axios from 'axios';

export default {
	localStorage: null,
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
	all(ordering = '-created') {
		const config = this.getRequestConfig();
		config.params = {
			ordering
		};
		return axios.get('/api/printers/', config)
			.then(response => {
				return response;
			});
	},
	get(uuid) {
		const config = this.getRequestConfig();
		return axios.get(`/api/printers/${uuid}/`, config)
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
	}
};
