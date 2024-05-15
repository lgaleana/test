describe('Overlay Text with Interact.js', () => {
  it('should allow dragging and dropping text over images', () => {
    cy.visit('/extract-content?url=https://example.com');
    cy.get('.draggable').first().trigger('mousedown', { which: 1 });
    cy.get('.draggable').first().trigger('mousemove', { clientX: 100, clientY: 100 });
    cy.get('.draggable').first().trigger('mouseup', { force: true });
    cy.get('.draggable').first().should('have.attr', 'style').and('include', 'transform: translate(100px, 100px)');
  });
});
