import test from 'ava';
import filter from '../src/components/scan.filter';

const scan = {
	nmap: {},
	scan: {
		'10.0.1.1': {
			tcp: {
				23: {state: 'open', product: ''},
				9100: {state: 'closed', product: 'HP 5020-NL'}
			}
		},
		'10.0.1.8': {
			tcp: {
				23: {state: 'closed', product: ''},
				9100: {state: 'closed', product: 'Brother 4002'}
			}
		}
	}
};

test('should filter to get data for bulk creation', t => {
	const printers = filter.printers(scan);

	t.deepEqual(printers, [
		{hostname: '10.0.1.1', port: 9100, description: 'HP 5020-NL'},
		{hostname: '10.0.1.8', port: 9100, description: 'Brother 4002'}
	]);
});
