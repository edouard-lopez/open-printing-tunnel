let EMPTY = 0;
describe('Tunnel action buttons', function() {
	beforeEach(function() {
		cy.server();
		cy.route('/api/sites/', 'fixture:new-site').as('getAllSites');
		cy.visit('/').closeSplash();
		cy.get('#notie-alert-outer').click({ force: true });
	});

	it('log tunnel start', function() {
		cy.route('PUT', '/api/sites/*/', { results: {} }).as('start');

		cy.get('[data-e2e=start]').click();

		cy.get('[data-e2e=stdout]')
			.children()
			.its('length')
			.should('be.gt', EMPTY);
	});

	it('log tunnel restart', function() {
		cy.route('PUT', '/api/sites/*/', { results: {} }).as('restart');

		cy.get('[data-e2e=restart]').click();

		cy.get('[data-e2e=stdout]')
			.children()
			.its('length')
			.should('be.gt', EMPTY);
	});

	it('log tunnel stop', function() {
		cy.route('PUT', '/api/sites/*/', { results: {} }).as('stop');

		cy.get('[data-e2e=stop]').click();

		cy.get('[data-e2e=stdout]')
			.children()
			.its('length')
			.should('be.gt', EMPTY);
	});

	it('log tunnel status', function() {
		cy.route('PUT', '/api/sites/*/', { results: {} }).as('status');

		cy.get('[data-e2e=status]').click();

		cy.get('[data-e2e=stdout]')
			.children()
			.its('length')
			.should('be.gt', EMPTY);
	});

	it('clear logs', function() {
		cy.route('PUT', '/api/sites/*/', { results: {} }).as('status');

		cy.get('[data-e2e=status]').click();

		cy.get('[data-e2e=stdout]').click();
		cy.get('[data-e2e=stdout]')
			.children()
			.its('length')
			.should('be', EMPTY);
	});
});
