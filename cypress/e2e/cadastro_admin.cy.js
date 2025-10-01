describe('Cadastro de Admin', () => {
    it('Deve preencher o formulário e retornar uma mensagem de sucesso', () => {
        cy.visit('http://localhost:3000/cadastro-admin')
        cy.get('input[name="nome"]').type('Ana Pereira')
        cy.get('input[name="email"]').type('ana@gmail.com')
        cy.get('input[name="dataNascimento"]').type('1992-07-25')
        cy.get('input[name="genero"]').select('Feminino')
        cy.get('input[name="cpf"]').type('11223344556')
        cy.get('input[name="senha"]').type('senhaSegura123')
        cy.get('input[name="confirmarSenha"]').type('senhaSegura123')
        cy.get('button[type="submit"]').click()
        cy.contains('Admin cadastrado com sucesso!').should('be.visible')
  })
});