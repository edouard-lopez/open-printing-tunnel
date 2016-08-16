import test from 'ava';
import printers from 'services/printers.service';

test('should parse a line', t => {
	const line = 'IMP RDC Couleur\t10.100.12.21';
	const parsedLine = printers.parseLine(line);

	t.deepEqual(parsedLine, {
		DESC: 'IMP RDC Couleur',
		PRINTER: '10.100.12.21',
		PORT: null
	});
});

test('should parse two lines', t => {
	const clipboard = 'IMP RDC Couleur\t10.100.12.21\nHP2055 Sylvie\t10.100.12.25';
	const parsedLines = printers.parsePrinters(clipboard);

	t.deepEqual(parsedLines, [
		{
			DESC: 'IMP RDC Couleur',
			PRINTER: '10.100.12.21',
			PORT: null
		},
		{
			DESC: 'HP2055 Sylvie',
			PRINTER: '10.100.12.25',
			PORT: null
		}
	]);
});

test('should parse port', t => {
	const line = 'Copieur Salle de reunion\t10.100.12.24\t9102';
	const parsedLine = printers.parseLine(line);

	t.deepEqual(parsedLine, {
		DESC: 'Copieur Salle de reunion',
		PRINTER: '10.100.12.24',
		PORT: '9102'
	});
});

test('should not parse empty string', t => {
	t.deepEqual(printers.parseLine(''), undefined);
});

test('should parse two printers', t => {
	const clipboard = '\nIMP RDC Couleur\t10.100.12.21\n\nHP2055 Sylvie\t10.100.12.25';
	const parsedLines = printers.parsePrinters(clipboard);

	t.is(2, parsedLines.length);
});
