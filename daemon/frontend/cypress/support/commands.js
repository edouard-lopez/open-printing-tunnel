Cypress.Commands.add("closeSplash", () => {
	cy.get("#splash .modal-header button").click();
});

Cypress.Commands.add("addNewSite", (id, hostname) => {
    cy.route("POST", "/api/sites/", {});
    
	cy.get("[data-e2e=add-site]").click();
	cy.get('[data-e2e="add-site:name"]').clear().type(id);
	cy.get('[data-e2e="add-site:hostname"]').clear().type(hostname);
	cy.get('[data-e2e="add-site:submit"]').click();
});
