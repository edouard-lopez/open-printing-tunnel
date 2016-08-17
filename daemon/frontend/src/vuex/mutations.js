import FileSaver from 'file-saver';

export default {
	setSites(state, sites) {
		state.sites = sites;
	},
	saveFile(response) {
		const filename = response.headers['content-disposition'].split('=')[1];
		console.log('saving: ', filename);
		const blob = new Blob([response.data], {type: response.headers['content-type']});
		FileSaver.saveAs(blob, filename);
	},
	clearLog(state) {
		console.log('mutation: clear')
		let empty = [];
		state.log = empty;
	},
	logResponse(state, response) {
		console.log('mutation: log')
		state.log = response.results;
	}
};
