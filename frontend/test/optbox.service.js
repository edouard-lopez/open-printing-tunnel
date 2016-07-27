import test from 'ava';
import nock from 'nock';

import optboxes from '../src/services/optboxes';
import {storageMock, optboxesGetAll, optboxGetOne} from './_helpers';

optboxes.localStorage = storageMock();

const token = 'ZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFt';
optboxes.localStorage.setItem('token', token);
const optbox = {
	location: 'nouvelle imprimante',
	name: '049fed91-6880-4c08-8cb2-21e8579d4543',
	address: '10.1.4.1'
};
test('should send requests with Authorization header', t => {
	const headers = {reqheaders: {Authorization: `JWT ${token}`}};
	nock('http://localhost/', headers).get('/api/optboxes/').query(true).reply(200, {});

	return optboxes.all().then(response => {
		t.is(response.status, 200);
	});
});

test('should create a optbox', t => {
	nock('http://localhost/').post('/api/optboxes/', optbox).reply(201, optbox);

	return optboxes.create(optbox).then(newPrinter => {
		t.truthy(newPrinter.address);
		t.is(newPrinter.address, '10.1.4.1');
	});
});

test('should send requests with Authorization header updated', t => {
	const newToken = 'WV9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRyd';
	optboxes.localStorage.setItem('token', newToken);
	const headers = {reqheaders: {Authorization: `JWT ${newToken}`}};
	nock('http://localhost/', headers).get('/api/optboxes/').query(true).reply(200, {});

	return optboxes.all().then(response => {
		t.is(response.status, 200);
	});
});

test('should get all optboxes with parameters', t => {
	nock('http://localhost/').get('/api/optboxes/?ordering=-created').reply(200, optboxesGetAll);

	return optboxes.all('-created').then(response => {
		t.is(response.status, 200);
		t.is(response.data.results.length, 3);
	});
});

test('should get a optbox', t => {
	nock('http://localhost/').get('/api/optboxes/049fed91-6880-4c08-8cb2-21e8579d4543/').reply(200, optboxGetOne);

	return optboxes.get('049fed91-6880-4c08-8cb2-21e8579d4543').then(optbox => {
		t.truthy(optboxGetOne.name);
		t.is(optboxGetOne.name, optbox.name);
	});
});

test('should update a optbox', t => {
	const updatedPrinter = JSON.parse(JSON.stringify(optboxGetOne));
	updatedPrinter.description = 'new description';
	nock('http://localhost/').put(`/api/optboxes/${updatedPrinter.id}/`).reply(200, updatedPrinter);

	return optboxes.update(updatedPrinter)
		.then(optbox => {
			t.is(optbox.address, '10.1.4.1');
		});
});

test('should delete a optbox', t => {
	nock('http://localhost/').delete(`/api/optboxes/${optboxGetOne.id}/`).reply(200);

	return optboxes.delete(optboxGetOne)
		.then(response => {
			t.is(response, '');
		});
});
