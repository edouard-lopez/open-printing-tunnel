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
		return axios.post('/daemon/optboxes/', optbox, config)
			.then(response => {
				return response.data;
			});
	},
	all() {
		const config = this.getRequestConfig();
		return axios.get('/daemon/optboxes/', config)
			.then(response => {
				return response;
			});
	},
	get(name) {
		const config = this.getRequestConfig();
		return axios.get(`/daemon/optboxes/${name}/`, config)
			.then(response => {
				return response.data;
			});
	},
	update(optbox) {
		const config = this.getRequestConfig();
		return axios.put(`/daemon/optboxes/${optbox.id}/`, optbox, config)
			.then(response => {
				return response.data;
			});
	},
	delete(optbox) {
		const config = this.getRequestConfig();
		return axios.delete(`/daemon/optboxes/${optbox.id}/`, config)
			.then(response => {
				return response.data;
			});
	}
};
