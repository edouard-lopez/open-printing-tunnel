export default {
	parseLine(line) {
		if (line) {
			const fields = line.split('\t');

			return {
				DESC: fields[0],
				PRINTER: fields[1],
				PORT: fields[2] || null
			};
		}
	},
	parsePrinters(clipboard) {
		return clipboard.split('\n')
			.filter(line => {
				return line;
			})
			.map(line => {
				return this.parseLine(line);
			});
	}
};
