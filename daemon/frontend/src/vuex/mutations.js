import FileSaver from 'file-saver';

export default {
	setSites(state, sites) {
		state.sites = sites;
	},
	saveFile({dispatch}, response) {
		const filename = response.headers['content-disposition'].split('=')[1];
		console.log('saving: ', filename);
		const blob = new Blob([response.data], {type: response.headers['content-type']});
		FileSaver.saveAs(blob, filename);
	}
};
