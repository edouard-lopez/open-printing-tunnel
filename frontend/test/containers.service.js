import test from 'ava';
import nock from 'nock';

import containers from '../src/services/containers';
import {storageMock, containersGetAll, containersGetOne} from './_helpers';

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
		t.is(container.login, newContainer.login);
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

test('should get all containers with offset', t => {
	nock('http://localhost/').get('/api/containers/').query(true).reply(200, {containers: containersGetAll});

	return containers.all().then(response => {
		t.is(response.status, 200);
		t.is(response.data.containers.results.length, containersGetAll.count);
	});
});

test('should get all containers with parameters', t => {
	nock('http://localhost/').get('/api/containers/?limit=100&offset=0&search=query&ordering=-created')
		.reply(200, {});

	return containers.all(100, 0, 'query', '-created').then(response => {
		t.is(response.status, 200);
	});
});

test('should get a container', t => {
	nock('http://localhost/').get('/api/containers/049fed91-6880-4c08-8cb2-21e8579d4543/').reply(200, containersGetOne);

	return containers.get('049fed91-6880-4c08-8cb2-21e8579d4543').then(container => {
		t.truthy(containersGetOne.company);
		t.is(containersGetOne.company, container.company);
	});
});

test('should update a container', t => {
	const updatedContainer = JSON.parse(JSON.stringify(containersGetOne));
	updatedContainer.description = 'new description';
	nock('http://localhost/').put(`/api/containers/${updatedContainer.id}/`).reply(200, updatedContainer);

	return containers.update(updatedContainer)
		.then(container => {
			t.is(updatedContainer.description, container.description);
		});
});

test('should delete a container', t => {
	nock('http://localhost/').delete(`/api/containers/${containersGetOne.id}/`).reply(200);

	return containers.delete(containersGetOne)
		.then(response => {
			t.is(response, '');
		});
});
