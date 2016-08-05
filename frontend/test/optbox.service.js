import test from 'ava';
import nock from 'nock';

import optboxesService from '../src/services/optboxes';
import {storageMock, optboxesGetAll, optboxGetOne} from './_helpers';

test('should remove optbox from list', t => {
	const optboxes = [{id: 4}, {id: 5}, {id: 15}];

	optboxesService.remove(optboxes, {id: 5});

	t.is(optboxes.length, 2);
	t.deepEqual(optboxes, [{id: 4}, {id: 15}]);
});

optboxesService.localStorage = storageMock();

const token = 'ZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFt';
optboxesService.localStorage.setItem('token', token);
const optbox = {
	location: 'nouveau boitier',
	id: '049fed91-6880-4c08-8cb2-21e8579d4543',
	hostname: '10.1.4.1'
};
test('should send requests with Authorization header', t => {
	const headers = {reqheaders: {Authorization: `JWT ${token}`}};
	nock('http://localhost/', headers).get('/daemon/optboxes/').query(true).reply(200, {});

	return optboxesService.all().then(response => {
		t.is(response.status, 200);
	});
});

test('should create a optbox', t => {
	nock('http://localhost/').post('/daemon/optboxes/', optbox).reply(201, optbox);

	return optboxesService.create(optbox).then(newPrinter => {
		t.truthy(newPrinter.hostname);
		t.is(newPrinter.hostname, '10.1.4.1');
	});
});

test('should send requests with Authorization header updated', t => {
	const newToken = 'WV9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRyd';
	optboxesService.localStorage.setItem('token', newToken);
	const headers = {reqheaders: {Authorization: `JWT ${newToken}`}};
	nock('http://localhost/', headers).get('/daemon/optboxes/').query(true).reply(200, {});

	return optboxesService.all().then(response => {
		t.is(response.status, 200);
	});
});

test('should get all optboxes with parameters', t => {
	nock('http://localhost/').get('/daemon/optboxes/').reply(200, optboxesGetAll);

	return optboxesService.all('-created').then(response => {
		t.is(response.status, 200);
		t.is(response.data.results.length, 3);
	});
});

test('should get a optbox', t => {
	nock('http://localhost/').get('/daemon/optboxes/049fed91-6880-4c08-8cb2-21e8579d4543/').reply(200, optboxGetOne);

	return optboxesService.get('049fed91-6880-4c08-8cb2-21e8579d4543').then(optbox => {
		t.truthy(optboxGetOne.id);
		t.is(optboxGetOne.id, optbox.id);
	});
});

test('should update a optbox', t => {
	const updatedPrinter = JSON.parse(JSON.stringify(optboxGetOne));
	updatedPrinter.description = 'new description';
	nock('http://localhost/').put(`/daemon/optboxes/${updatedPrinter.id}/`).reply(200, updatedPrinter);

	return optboxesService.update(updatedPrinter)
		.then(optbox => {
			t.is(optbox.hostname, 'bordeaux.opt');
		});
});

test('should delete a optbox', t => {
	nock('http://localhost/').delete(`/daemon/optboxes/${optboxGetOne.id}/`).reply(200);

	return optboxesService.delete(optboxGetOne)
		.then(response => {
			t.is(response, '');
		});
});
