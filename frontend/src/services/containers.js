import axios from 'axios';

export default {
	localStorage: null,
	getRequestConfig() {
		const token = this.localStorage.getItem('token');
		return {
			headers: {Authorization: `JWT ${token}`}
		};
	},
	create(container) {
		const config = this.getRequestConfig();
		return axios.post('/api/mast-containers/', container, config)
			.then(response => {
				return response.data;
			});
	},
	all(limit = 20, offset = 0, search = '', ordering = '-created') {
		const config = this.getRequestConfig();
		config.params = {
			limit,
			offset,
			search,
			ordering
		};
		return axios.get('/api/mast-containers/', config)
			.then(response => {
				return response;
			});
	},
	get(uuid) {
		const config = this.getRequestConfig();
		return axios.get(`/api/mast-containers/${uuid}/`, config)
			.then(response => {
				return response.data;
			});
	},
	update(container) {
		const config = this.getRequestConfig();
		return axios.put(`/api/mast-containers/${container.id}/`, container, config)
			.then(response => {
				return response.data;
			});
	},
	delete(container) {
		const config = this.getRequestConfig();
		return axios.delete(`/api/mast-containers/${container.id}/`, config)
			.then(response => {
				return response.data;
			});
	}
};
