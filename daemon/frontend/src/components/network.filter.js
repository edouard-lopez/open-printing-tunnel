export default {
	icon(value, type) {
//				let icon = 'fa-pulsing fa-fw text-warning';
		let icon = 'fa-warning text-warning';

		if (type === 'ping' && value > 0) {
			icon = 'fa-check text-success';
		} else if (type === 'telnet' && value) {
			icon = 'fa-check text-primary';
		}

		return icon;
	},
	reachable(value) {
		return value ? 'accessible' : 'indisponible';
	}
};
