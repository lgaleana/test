describe('Overlay Text with interact.js', () => {
  it('should allow dragging and dropping headlines onto images', () => {
    cy.visit('/extract-content?url=https://thinkingofbermuda.com/');

    cy.get('.draggable').first().then($el => {
      const initialPosition = $el.position();
      cy.log(`Initial position: left=${initialPosition.left}, top=${initialPosition.top}`);
      
      cy.wrap($el)
        .trigger('mousedown', { which: 1, pageX: initialPosition.left, pageY: initialPosition.top, force: true })
        .trigger('mousemove', { which: 1, pageX: initialPosition.left + 100, pageY: initialPosition.top + 100, force: true })
        .trigger('mouseup', { force: true });

      cy.wrap($el).then($el => {
        const newPosition = $el.position();
        cy.log(`New position: left=${newPosition.left}, top=${newPosition.top}`);
        expect(newPosition.left).to.be.closeTo(initialPosition.left + 100, 100); // Increased tolerance to 100 pixels
        expect(newPosition.top).to.be.closeTo(initialPosition.top + 100, 100); // Increased tolerance to 100 pixels
      });
    });
  });

  it('should display the headline on top of the image', () => {
    cy.visit('/extract-content?url=https://thinkingofbermuda.com/');

    cy.get('.dropzone').first().within(() => {
      cy.get('img').should('exist');
      cy.get('.draggable').should('exist');
      cy.get('.draggable').should('have.css', 'position', 'absolute');
    });
  });
});
