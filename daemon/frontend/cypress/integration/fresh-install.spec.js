describe('Fresh install', function() {
  it('alert about failing to fetch sites', function() {
    cy.server();
    cy.route('/api/sites/', {}).as('getAllSites');

    cy.visit('/').closeSplash();

    cy.wait('@getAllSites')
      .its('status')
      .should('eq', 200);
    cy.get('#notie-alert-outer').should('be.visible');
    cy.get('#notie-alert-outer').click();
  });
  it('has a header card', function() {
    cy.get('[data-e2e=header]').contains('Sites');
  });
  it('has a button to add site', function() {
    cy.get('[data-e2e=add-site]').contains('Ajouter un site');
  });
  it('shows "no sites detected" message', function() {
    cy.get('[data-e2e=no-site-available]').contains('Aucun site détecté…');
  });
});
