import test from 'ava';
import printers from '../src/services/printers.service';

test('should parse a line', t => {
	const line = 'IMP RDC Couleur\t10.100.12.21';
	const parsedLine = printers.parseLine(line);

	t.deepEqual(parsedLine, {
		description: 'IMP RDC Couleur',
		hostname: '10.100.12.21',
		port: null
	});
});

test('should parse two lines', t => {
	const clipboard =
		'IMP RDC Couleur\t10.100.12.21\nHP2055 Sylvie\t10.100.12.25';
	const parsedLines = printers.parsePrinters(clipboard);

	t.deepEqual(parsedLines, [
		{
			description: 'IMP RDC Couleur',
			hostname: '10.100.12.21',
			port: null
		},
		{
			description: 'HP2055 Sylvie',
			hostname: '10.100.12.25',
			port: null
		}
	]);
});

test('should parse port', t => {
	const line = 'Copieur Salle de reunion\t10.100.12.24\t9102';
	const parsedLine = printers.parseLine(line);

	t.deepEqual(parsedLine, {
		description: 'Copieur Salle de reunion',
		hostname: '10.100.12.24',
		port: '9102'
	});
});

test('should not parse empty string', t => {
	t.deepEqual(printers.parseLine(''), undefined);
});

test('should parse two printers', t => {
	const clipboard =
		'\nIMP RDC Couleur\t10.100.12.21\n\nHP2055 Sylvie\t10.100.12.25';
	const parsedLines = printers.parsePrinters(clipboard);

	t.is(2, parsedLines.length);
});
