import test from 'ava';
import Network from '../src/pages/networks/network';

test('should add a lowercase `id` copied from `Id`', t => {
	const networks = [{Id: 'ec0a7'}, {Id: '804e6'}];

	const new_networks = Network.addLowercaseId(networks);

	t.deepEqual(new_networks, [
		{Id: 'ec0a7', id: 'ec0a7'},
		{Id: '804e6', id: '804e6'}
	]);
});

test('should tell is there is containers or not', t => {
	const with_containers = {Containers: {a: 1, b: 2}};
	const without_containers = {Containers: {}};

	t.is(Network.isEmptyNetwork(with_containers), false);
	t.is(Network.isEmptyNetwork(without_containers), true);
});
