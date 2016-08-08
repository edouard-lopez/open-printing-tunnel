import test from 'ava';
import nock from 'nock';

import '../src/services/array.polyfill';
import printersService from '../src/services/printers.service';
import {storageMock, printersGetAll, printerGetOne} from './_helpers';

test('should remove printer from list', t => {
	const printers = [{id: 4}, {id: 5}, {id: 15}];

	const newPrinters = printersService.remove(printers, 5);

	t.is(newPrinters.length, 2);
	t.deepEqual(newPrinters, [{id: 4}, {id: 15}]);
});

printersService.localStorage = storageMock();

const token = 'ZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFt';
printersService.localStorage.setItem('token', token);
const printer = {
	id: 'nouvelle imprimante',
	hostname: '1.2.3.4',
	description: 'salle de réunion'
};
test('should send requests with Authorization header', t => {
	const headers = {reqheaders: {Authorization: `JWT ${token}`}};
	nock('http://localhost/', headers).get('/daemon/printers/').query(true).reply(200, {});

	return printersService.all().then(response => {
		t.truthy(response);
	});
});

test('should create a printer', t => {
	nock('http://localhost/').post('/daemon/printers/', printer).reply(201, printer);

	return printersService.create(printer).then(newPrinter => {
		t.truthy(newPrinter.hostname);
		t.is(newPrinter.hostname, '1.2.3.4');
	});
});

test('should send requests with Authorization header updated', t => {
	const newToken = 'WV9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRyd';
	printersService.localStorage.setItem('token', newToken);
	const headers = {reqheaders: {Authorization: `JWT ${newToken}`}};
	nock('http://localhost/', headers).get('/daemon/printers/').query(true).reply(200, {});

	return printersService.all().then(response => {
		t.truthy(response);
	});
});

test('should get all printers with parameters', t => {
	nock('http://localhost/').get('/daemon/printers/').reply(200, printersGetAll);

	return printersService.all().then(response => {
		t.is(response.data.length, 3);
	});
});

test('should get a printer', t => {
	nock('http://localhost/').get('/daemon/printers/049fed91-6880-4c08-8cb2-21e8579d4543/').reply(200, printerGetOne);

	return printersService.get('049fed91-6880-4c08-8cb2-21e8579d4543').then(printer => {
		t.is(printerGetOne.id, 0);
		t.is(printerGetOne.id, printer.id);
	});
});

test('should update a printer', t => {
	const updatedPrinter = JSON.parse(JSON.stringify(printerGetOne));
	updatedPrinter.description = 'new description';
	nock('http://localhost/').put(`/daemon/printers/${updatedPrinter.id}/`).reply(200, updatedPrinter);

	return printersService.update(updatedPrinter)
		.then(printer => {
			t.is(printer.hostname, '1.2.3.4');
		});
});

test('should delete a printer', t => {
	nock('http://localhost/').delete(`/daemon/printers/${printerGetOne.id}/`).reply(200);

	return printersService.delete(printerGetOne)
		.then(response => {
			t.is(response, '');
		});
});
