import test from 'ava';
import nock from 'nock';

import printers from '../src/services/printers';
import {storageMock, printersGetAll, printersGetOne} from './_helpers';

printers.localStorage = storageMock();

const token = 'ZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFt';
printers.localStorage.setItem('token', token);
const printer = {
	location: 'nouvelle imprimante',
	opt_box: '049fed91-6880-4c08-8cb2-21e8579d4543',
	address: '10.1.4.1'
};
test('should send requests with Authorization header', t => {
	const headers = {reqheaders: {Authorization: `JWT ${token}`}};
	nock('http://localhost/', headers).get('/api/printers/').query(true).reply(200, {});

	return printers.all().then(response => {
		t.is(response.status, 200);
	});
});

test('should create a printer', t => {
	nock('http://localhost/').post('/api/printers/', printer).reply(201, printer);

	return printers.create(printer).then(newPrinter => {
		t.truthy(newPrinter.address);
		t.is(newPrinter.address, '10.1.4.1');
	});
});

test('should send requests with Authorization header updated', t => {
	const newToken = 'WV9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRyd';
	printers.localStorage.setItem('token', newToken);
	const headers = {reqheaders: {Authorization: `JWT ${newToken}`}};
	nock('http://localhost/', headers).get('/api/printers/').query(true).reply(200, {});

	return printers.all().then(response => {
		t.is(response.status, 200);
	});
});

test('should get all printers with parameters', t => {
	nock('http://localhost/').get('/api/printers/?ordering=-created').reply(200, printersGetAll);

	return printers.all('-created').then(response => {
		t.is(response.status, 200);
		t.is(response.data.results.length, 3);
	});
});

test('should get a printer', t => {
	nock('http://localhost/').get('/api/printers/049fed91-6880-4c08-8cb2-21e8579d4543/').reply(200, printersGetOne);

	return printers.get('049fed91-6880-4c08-8cb2-21e8579d4543').then(printer => {
		t.truthy(printersGetOne.opt_box);
		t.is(printersGetOne.opt_box, printer.opt_box);
	});
});

test('should update a printer', t => {
	const updatedPrinter = JSON.parse(JSON.stringify(printersGetOne));
	updatedPrinter.description = 'new description';
	nock('http://localhost/').put(`/api/printers/${updatedPrinter.id}/`).reply(200, updatedPrinter);

	return printers.update(updatedPrinter)
		.then(printer => {
			t.is(printer.address, '10.1.4.1');
		});
});

test('should delete a printer', t => {
	nock('http://localhost/').delete(`/api/printers/${printersGetOne.id}/`).reply(200);

	return printers.delete(printersGetOne)
		.then(response => {
			t.is(response, '');
		});
});
