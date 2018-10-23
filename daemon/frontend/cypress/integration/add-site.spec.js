describe('Add site', function() {
    beforeEach(function(){
        cy.server()
        cy.route('/api/sites/', {}).as('getAllSites')
        cy.visit('/').closeSplash()
        cy.get('#notie-alert-outer').click()
    })
    
    it('open dialog to add site', function() {
        cy.get('[data-e2e=add-site]').click()

        cy.get('[data-e2e=add-site-modal]').should('have.class', 'in')
    })

    it('close new site dialog', function() {
        cy.get('[data-e2e=add-site]').click()
        cy.get('[data-e2e=add-site-modal] .modal-header [data-dismiss]').click()
        cy.get('[data-e2e=add-site-modal]').should('not.have.class', 'in')

        cy.get('[data-e2e=add-site]').click()
        cy.get('[data-e2e=add-site-modal] .modal-footer [data-dismiss]').click()
        cy.get('[data-e2e=add-site-modal]').should('not.have.class', 'in')
    })

    it('fill new site dialog', function() {
        cy.route({
            method: 'POST',
            url: '/api/sites/',
            response: {},
            delay: 100
          }).as('newSite')

        cy.get('[data-e2e=add-site]').click()
        cy.get('[data-e2e="add-site:name"]').clear().type('test-site')
        cy.get('[data-e2e="add-site:hostname"]').clear().type('0.0.0.0')
          
        cy.get('[data-e2e="add-site:submit"]').click().contains('Création en cours')
    })

    it('create a new site', function() {
        cy.route('POST', '/api/sites/', {})
        cy.route('/api/sites/', 'fixture:new-site')

        cy.addNewSite('test-site', '0.0.0.0')
        cy.get('[data-e2e="no-site-available"]').should('not.be.visible')
        cy.get('[data-e2e="sites"]').children().should('have.length', 1)
    })    
})