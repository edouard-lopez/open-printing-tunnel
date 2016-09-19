import test from 'ava';
import axios from 'axios';
import nock from 'nock';
import http from '../src/services/http.service';
import {storageMock} from './_helpers';

axios.defaults.baseURL = 'http://localhost/';
const foos = http('foos', storageMock());

const token = 'ZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFt';
foos.localStorage.setItem('token', token);
/* eslint camelcase: 0 */
const foo = {
	name: 'foo'
};

test('should send requests with Authorization header', t => {
	const headers = {reqheaders: {Authorization: `JWT ${token}`}};
	nock('http://localhost/', headers).get('/api/foos/').query(true).reply(200, {});
	return foos.all().then(response => {
		t.is(response.status, 200);
	});
});

test('should create a foo', t => {
	nock('http://localhost/').post('/api/foos/', foo).reply(201, foo);
	return foos.create(foo).then(response => {
		const newIncident = response.data;
		t.is(foo.login, newIncident.login);
	});
});

test('should send requests with Authorization header updated', t => {
	const newToken = 'WV9eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRyd';
	foos.localStorage.setItem('token', newToken);
	const headers = {reqheaders: {Authorization: `JWT ${newToken}`}};
	nock('http://localhost/', headers).get('/api/foos/').query(true).reply(200, {});
	return foos.all().then(response => {
		t.is(response.status, 200);
	});
});

test('should get all foo with parameters', t => {
	nock('http://localhost/').get('/api/foos/?limit=100&offset=0&search=query&ordering=-created')
		.reply(200, {});
	const params = {limit: 100, offset: 0, search: 'query', ordering: '-created'};
	return foos.all(params).then(response => {
		t.is(response.status, 200);
	});
});
