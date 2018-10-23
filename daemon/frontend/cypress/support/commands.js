Cypress.Commands.add('closeSplash', () => {
    cy.get('#splash .modal-header button').click()
})