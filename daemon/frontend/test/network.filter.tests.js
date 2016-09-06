import test from 'ava';
import network from '../src/components/network.filter';

test('should use yellow-warning icon when ping or telnet fails', t => {
	const probe = 0;
	const ping = network.icon(probe, 'ping');
	t.is(ping, 'fa-warning text-warning');
});

test('should use green-check icon when pingable', t => {
	const probe = 123;
	const ping = network.icon(probe, 'ping');
	t.is(ping, 'fa-check text-success');
});

test('should use blue-check icon when reachable by telnet', t => {
	const probe = true;
	const telnet = network.icon(probe, 'telnet');
	t.is(telnet, 'fa-check text-primary');
});

test('should label as "accessible" when reachable', t => {
	t.is(network.reachable(true), 'accessible');
});

test('should label as "indisponible" when reachable', t => {
	t.is(network.reachable(false), 'indisponible');
});
