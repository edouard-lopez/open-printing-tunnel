import axios from 'axios';

export default {
	localStorage: null,
	getRequestConfig() {
		const token = this.localStorage.getItem('token');
		return {
			headers: {Authorization: `JWT ${token}`}
		};
	},
	create(optbox) {
		const config = this.getRequestConfig();
		return axios.post('/api/optboxes/', optbox, config)
			.then(response => {
				return response.data;
			});
	},
	all(ordering = '-created') {
		const config = this.getRequestConfig();
		config.params = {
			ordering
		};
		return axios.get('/api/optboxes/', config)
			.then(response => {
				return response;
			});
	},
	get(uuid) {
		const config = this.getRequestConfig();
		return axios.get(`/api/optboxes/${uuid}/`, config)
			.then(response => {
				return response.data;
			});
	},
	update(optbox) {
		const config = this.getRequestConfig();
		return axios.put(`/api/optboxes/${optbox.id}/`, optbox, config)
			.then(response => {
				return response.data;
			});
	},
	delete(optbox) {
		const config = this.getRequestConfig();
		return axios.delete(`/api/optboxes/${optbox.id}/`, config)
			.then(response => {
				return response.data;
			});
	}
};
