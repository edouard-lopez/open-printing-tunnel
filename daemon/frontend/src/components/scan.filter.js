export default {
	getPrinter(ports, hostname) {
		for (const port in ports) {
			if ({}.hasOwnProperty.call(ports, port) && parseInt(port, 10) === 9100) {
				const details = ports[port];
				return {
					hostname,
					port: parseInt(port, 10),
					description: details ? details.product : ''
				};
			}
		}
		return null;
	},
	printers(nmap) {
		const printers = [];

		const devices = nmap.scan;

		for (const hostname in devices) {
			if ({}.hasOwnProperty.call(devices, hostname)) {
				const ports = devices[hostname].tcp;
				const printer = this.getPrinter(ports, hostname);
				if (printer) {
					printers.push(printer);
				}
			}
		}
		return printers;
	},
	clipboard(printers) {
		return printers.map(printer => [printer.description, printer.hostname, printer.port].join('\t'));
	}
};
