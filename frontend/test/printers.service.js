import test from 'ava';
import nock from 'nock';

import printers from '../src/services/printers';
import {storageMock, printersGetAll, printerGetOne} from './_helpers';

printers.localStorage = storageMock();

const token = 'ZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFt';
printers.localStorage.setItem('token', token);
const printer = {
	name: 'nouvelle imprimante',
	hostname: '1.2.3.4',
	description: 'salle de réunion',
};
test('should send requests with Authorization header', t => {
	const headers = {reqheaders: {Authorization: `JWT ${token}`}};
	nock('http://localhost/', headers).get('/daemon/printers/').query(true).reply(200, {});

	return printers.all().then(response => {
		t.is(response.status, 200);
	});
});

test('should create a printer', t => {
	nock('http://localhost/').post('/daemon/printers/', printer).reply(201, printer);

	return printers.create(printer).then(newPrinter => {
		t.truthy(newPrinter.hostname);
		t.is(newPrinter.hostname, '1.2.3.4');
	});
});

test('should send requests with Authorization header updated', t => {
	const newToken = 'WV9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRyd';
	printers.localStorage.setItem('token', newToken);
	const headers = {reqheaders: {Authorization: `JWT ${newToken}`}};
	nock('http://localhost/', headers).get('/daemon/printers/').query(true).reply(200, {});

	return printers.all().then(response => {
		t.is(response.status, 200);
	});
});

test('should get all printers with parameters', t => {
	nock('http://localhost/').get('/daemon/printers/?ordering=-created').reply(200, printersGetAll);

	return printers.all('-created').then(response => {
		t.is(response.status, 200);
		t.is(response.data.results.length, 3);
	});
});

test('should get a printer', t => {
	nock('http://localhost/').get('/daemon/printers/049fed91-6880-4c08-8cb2-21e8579d4543/').reply(200, printerGetOne);

	return printers.get('049fed91-6880-4c08-8cb2-21e8579d4543').then(printer => {
		t.truthy(printerGetOne.name);
		t.is(printerGetOne.name, printer.name);
	});
});

test('should update a printer', t => {
	const updatedPrinter = JSON.parse(JSON.stringify(printerGetOne));
	updatedPrinter.description = 'new description';
	nock('http://localhost/').put(`/daemon/printers/${updatedPrinter.id}/`).reply(200, updatedPrinter);

	return printers.update(updatedPrinter)
		.then(printer => {
			t.is(printer.hostname, '1.2.3.4');
		});
});

test('should delete a printer', t => {
	nock('http://localhost/').delete(`/daemon/printers/${printerGetOne.id}/`).reply(200);

	return printers.delete(printerGetOne)
		.then(response => {
			t.is(response, '');
		});
});
