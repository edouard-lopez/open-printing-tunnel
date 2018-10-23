export default {
	toLog(printers) {
		const log = [];

		for (const hostname in printers) {
			if ({}.hasOwnProperty.call(printers, hostname)) {
				const printer = printers[hostname];
				log.push(
					[
						printer.description.value,
						printer.hostname,
						printer.port,
						'# pageCount: ' + printer.pageCount.value,
						'sysContact: ' + printer.sysContact.value,
						'sysDescription: ' + printer.sysDescription.value,
						'sysName: ' + printer.sysName.value,
						'uptime: ' + printer.uptime.value
					].join('\t')
				);
			}
		}
		return log;
	},
	toClipboard(printers) {
		const log = [];

		for (const hostname in printers) {
			if ({}.hasOwnProperty.call(printers, hostname)) {
				const printer = printers[hostname];
				log.push(
					[printer.description.value, printer.hostname, printer.port].join('\t')
				);
			}
		}
		return log;
	},
	text(clipboard = []) {
		let multilines = '';

		multilines = clipboard.join('\n');

		return multilines;
	}
};
