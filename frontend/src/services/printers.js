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
		return axios.post('/daemon/printers/', printer, config)
			.then(response => {
				return response.data;
			});
	},
	all(ordering = '-created') {
		const config = this.getRequestConfig();
		config.params = {
			ordering
		};
		return axios.get('/daemon/printers/', config)
			.then(response => {
				return response;
			});
	},
	get(uuid) {
		const config = this.getRequestConfig();
		return axios.get(`/daemon/printers/${uuid}/`, config)
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
	}
};
