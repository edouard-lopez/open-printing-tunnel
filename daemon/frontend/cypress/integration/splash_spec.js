describe('Splash warning', function() {
    context('Splash', function(){
        beforeEach(function(){
          cy.visit('/')
    })
        it('is visible', function() {
            cy.get('#splash').should('be.visible')
            cy.get('#splash .modal-header button').should('be.visible')
            cy.get('#splash .modal-footer button').contains('Accepter').and('be.visible')
        })
        it('can be closed by x', function() {
            cy.get('#splash .modal-header button').click().should('not.be.visible')
        })
        it('can be closed by accept button', function() {
            cy.get('#splash .modal-footer button').click().should('not.be.visible')
        })
    });
})