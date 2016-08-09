import nock from 'nock';
import test from 'ava';
import resource from 'pilou';
import sitesService from '../src/services/sites.service';
import {sitesGetAll, siteGetOne} from './_helpers';

const sites = resource('sites', {
	all: '/daemon/${resource}/',
	create: '/daemon/${resource}/',
	delete: '/daemon/${resource}/${site_id}/',
	get: '/daemon/${resource}/${site_id}/',
	update: '/daemon/${resource}/${site_id}/'
});

test('should find site index in list', t => {
	const sites = [{id: 'akema'}, {id: 'coaxis'}, {id: 'github'}];
	let siteIndex = -1;

	siteIndex = sitesService.getIndex(sites, 'github');

	t.is(siteIndex, 2);
});

test('should remove site from list', t => {
	const sites = [{id: 'akema'}, {id: 'coaxis'}, {id: 'github'}];

	sitesService.remove(sites, {id: 'coaxis'});

	t.is(sites.length, 2);
	t.deepEqual(sites, [{id: 'akema'}, {id: 'github'}]);
});

test('should create a site', t => {
	const site = {
		name: 'Bordeaux',
		hostname: '10.0.0.1'
	};
	nock('http://localhost/').post('/daemon/sites/', site).reply(201, siteGetOne);

	return sites.create(site).then(response => {
		t.is(response.data.id, 'bordeaux');
		t.is(response.data.hostname, '10.0.0.1');
	});
});

test('should get all sites with parameters', t => {
	nock('http://localhost/').get('/daemon/sites/').reply(200, sitesGetAll);

	return sites.all('-created').then(response => {
		t.is(response.status, 200);
		t.is(response.data.results.length, 3);
	});
});

test('should get a site', t => {
	nock('http://localhost/').get('/daemon/sites/bordeaux/').reply(200, siteGetOne);

	return sites.get({site_id: 'bordeaux'}).then(response => {
		t.is(response.data.id, 'bordeaux');
	});
});

test('should update a site', t => {
	nock('http://localhost/').put(`/daemon/sites/${siteGetOne.id}/`).reply(200, siteGetOne);
	return sites.update({site_id: siteGetOne.id}, {action: 'start'}).then(response => {
		t.is(response.data.hostname, '10.0.0.1');
	});
});

test('should delete a site', t => {
	nock('http://localhost/').delete(`/daemon/sites/${siteGetOne.id}/`).reply(200);

	return sites.delete({site_id: siteGetOne.id}).then(response => {
		t.is(response.status, 200);
	});
});
