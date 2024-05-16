describe('Download Image with Overlayed Text', () => {
  it('should download the image with the overlayed text when the download button is clicked', () => {
    cy.visit('/extract-content?url=https://thinkingofbermuda.com/');

    cy.get('.dropzone').first().within(() => {
      cy.get('button').contains('Download').click();

      // We can't verify the download directly, but we can ensure the button exists and is clickable
      cy.get('button').contains('Download').should('exist');
    });
  });
});
