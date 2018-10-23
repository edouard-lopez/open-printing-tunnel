export default {
  parseLine(line) {
    if (line) {
      const fields = line.split('\t');

      return {
        description: fields[0],
        hostname: fields[1],
        port: fields[2] || null
      };
    }
  },
  parsePrinters(clipboard) {
    return clipboard
      .split('\n')
      .filter(line => {
        return line;
      })
      .map(line => {
        return this.parseLine(line);
      });
  }
};
