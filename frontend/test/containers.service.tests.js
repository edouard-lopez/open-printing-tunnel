import test from 'ava';
import nock from 'nock';

import containers from '../src/services/containers.service';
import {storageMock} from './_helpers';

containers.localStorage = storageMock();

const token = 'ZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFt';
containers.localStorage.setItem('token', token);
const container = {
	description: 'my new container'
};
test('should send requests with Authorization header', t => {
	const headers = {reqheaders: {Authorization: `JWT ${token}`}};
	nock('http://localhost/', headers).get('/api/containers/').query(true).reply(200, {});

	return containers.all().then(response => {
		t.is(response.status, 200);
	});
});

test('should create a container', t => {
	nock('http://localhost/').post('/api/containers/', container).reply(201, container);

	return containers.create(container).then(newContainer => {
		t.truthy(newContainer.description);
		t.is(newContainer.description, 'my new container');
	});
});

test('should send requests with Authorization header updated', t => {
	const newToken = 'WV9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRyd';
	containers.localStorage.setItem('token', newToken);
	const headers = {reqheaders: {Authorization: `JWT ${newToken}`}};
	nock('http://localhost/', headers).get('/api/containers/').query(true).reply(200, {});

	return containers.all().then(response => {
		t.is(response.status, 200);
	});
});
