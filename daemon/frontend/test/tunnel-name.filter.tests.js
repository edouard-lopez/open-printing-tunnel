import test from 'ava';
import tunnelName from '../src/components/tunnel-name.filter';

test('format speed equal to zero', t => {
  const speed = tunnelName.kb(0);
  t.is(speed, '0 Kb/s');
});

test('format positive speed', t => {
  const speed = tunnelName.kb(150);
  t.is(speed, '150 Kb/s');
});

test('Split big number', t => {
  const speed = tunnelName.kb(10000000);
  t.is(speed, '10 000 000 Kb/s');
});
