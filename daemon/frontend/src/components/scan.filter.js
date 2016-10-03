export default {
	clipboard(printers) {
		const clipboard = [];

		for (const hostname in printers) {
			if ({}.hasOwnProperty.call(printers, hostname)) {
				const printer = printers[hostname];
				clipboard.push([printer.description.value, printer.hostname, printer.port].join('\t'));
			}
		}
		return clipboard;
	}
};
