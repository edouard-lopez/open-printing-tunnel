import test from 'ava';
import filter from '../src/components/scan.filter';

test('should get printer', t => {
	const hostname = '10.0.1.2';
	const ports = {9100: {state: 'closed', product: 'HP 5020-NL'}};

	const printer = filter.getPrinter(ports, hostname);

	t.deepEqual(printer, {hostname: '10.0.1.2', port: 9100, description: 'HP 5020-NL'});
});

test('should ignore non-printer', t => {
	const hostname = '10.0.1.2';
	const ports = {23: {state: 'closed', product: ''}};

	const printer = filter.getPrinter(ports, hostname);

	t.is(printer, null);
});

test('should filter to get data for bulk creation', t => {
	const scan = {scan: {'10.0.1.1': {tcp: {9100: {state: 'closed', product: 'HP 5020-NL'}}}}};

	const printers = filter.printers(scan);

	t.is(printers.length, 1);
	t.deepEqual(printers, [{hostname: '10.0.1.1', port: 9100, description: 'HP 5020-NL'}]);
});

test('should format as raw text clipboard content', t => {
	const printers = [{hostname: '10.0.1.1', port: 9100, description: 'HP 5020-NL'}];

	const clipboard = filter.clipboard(printers);

	t.deepEqual(clipboard, ['HP 5020-NL\t10.0.1.1\t9100']);
});
test('should format with empty description', t => {
	const printers = [{hostname: '10.0.1.8', port: 9100, description: ''}];

	const clipboard = filter.clipboard(printers);

	t.deepEqual(clipboard, ['\t10.0.1.8\t9100']);
});
