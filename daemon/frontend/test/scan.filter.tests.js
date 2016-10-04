import test from 'ava';
import filter from '../src/components/scan.filter';
import scan from './nmap_snmp.mock.json';

test('should format as raw text clipboard content', t => {
	const printers = {
		'192.168.2.250': {
			hostname: '192.168.2.250',
			port: 9100,
			description: {value: 'Brother HL-5250DN series'}
		}
	};

	const clipboard = filter.clipboard(printers);

	t.deepEqual(clipboard, ['Brother HL-5250DN series\t192.168.2.250\t9100']);
});
test('should format with empty description', t => {
	const printers = {
		'192.168.2.250': {
			hostname: '192.168.2.250',
			port: 9100,
			description: {value: ''}
		}
	};
	const clipboard = filter.clipboard(printers);

	t.deepEqual(clipboard, ['\t192.168.2.250\t9100']);
});

test('should format to log', t => {
	const printers = scan.devices;

	const clipboard = filter.clipboard(printers);

	t.deepEqual(clipboard, [
		'Brother HL-5250DN series\t192.168.2.250\t9100'
	]);
});
