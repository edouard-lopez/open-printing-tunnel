export default {
	printers(nmap) {
		const printers = [];

		const devices = nmap.scan;
		console.log('devices', devices);
		for (const hostname in devices) {
			if ({}.hasOwnProperty.call(devices, hostname)) {
				const port = 9100;

				printers.push(
					{
						hostname,
						port,
						description: devices[hostname].tcp[port].product || null
					}
				);
			}
		}
		return printers;
	}
};
