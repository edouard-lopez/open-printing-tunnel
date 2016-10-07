export default {
	clipboard(printers) {
		const clipboard = [];

		for (const hostname in printers) {
			if ({}.hasOwnProperty.call(printers, hostname)) {
				const printer = printers[hostname];
				clipboard.push([
					printer.description.value,
					printer.hostname,
					printer.port,
					'# pageCount: ' + printer.pageCount.value,
					'sysContact: ' + printer.sysContact.value,
					'sysDescription: ' + printer.sysDescription.value,
					'sysName: ' + printer.sysName.value,
					'uptime: ' + printer.uptime.value
				].join('\t'));
			}
		}
		return clipboard;
	},
	text(clipboard) {
		let multilines = '';

		multilines = clipboard.join('\n');

		return multilines;
	}
};
