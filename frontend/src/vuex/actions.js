import http from '../services/http.service';

const DaemonService = http('daemons', localStorage);

export default {
	fetchDaemon({dispatch}, id) {
		DaemonService.get({id}).then(response => {
			dispatch('SET_DAEMON', response.data);
		});
	}
};
