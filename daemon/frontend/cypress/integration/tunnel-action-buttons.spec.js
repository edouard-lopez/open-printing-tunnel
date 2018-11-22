describe('Tunnel action buttons', function() {
	let EMPTY_JOURNAL = 0;
	const MOCK_RESPONSE = { results: {} };

	beforeEach(function() {
		cy.server();
		cy.route('/api/sites/', 'fixture:new-site').as('getAllSites');
		cy.visit('/').closeSplash();
		cy.get('#notie-alert-outer').click({ force: true });
	});

	it('log tunnel start', function() {
		cy.route('PUT', '/api/sites/*/', MOCK_RESPONSE).as('start');

		cy.get('[data-e2e=start]').click();

		cy.get('[data-e2e=stdout]')
			.children()
			.its('length')
			.should('be.gt', EMPTY_JOURNAL);
	});

	it('log tunnel restart', function() {
		cy.route('PUT', '/api/sites/*/', MOCK_RESPONSE).as('restart');

		cy.get('[data-e2e=restart]').click();

		cy.get('[data-e2e=stdout]')
			.children()
			.its('length')
			.should('be.gt', EMPTY_JOURNAL);
	});

	it('log tunnel stop', function() {
		cy.route('PUT', '/api/sites/*/', MOCK_RESPONSE).as('stop');

		cy.get('[data-e2e=stop]').click();

		cy.get('[data-e2e=stdout]')
			.children()
			.its('length')
			.should('be.gt', EMPTY_JOURNAL);
	});

	it('log tunnel status', function() {
		cy.route('PUT', '/api/sites/*/', MOCK_RESPONSE).as('status');

		cy.get('[data-e2e=status]').click();

		cy.get('[data-e2e=stdout]')
			.children()
			.its('length')
			.should('be.gt', EMPTY_JOURNAL);
	});

	it('clear logs', function() {
		cy.route('PUT', '/api/sites/*/', MOCK_RESPONSE).as('status');

		cy.get('[data-e2e=status]').click();

		cy.get('[data-e2e=stdout]').click();
		cy.get('[data-e2e=stdout]')
			.children()
			.its('length')
			.should('be', EMPTY_JOURNAL);
	});
});
