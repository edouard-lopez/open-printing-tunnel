export default {
	kb(value) {
		const speed = String(value).replace(/(.)(?=(\d{3})+$)/g, '$1 ');
		return `${speed} Kb/s`;
	}
};
