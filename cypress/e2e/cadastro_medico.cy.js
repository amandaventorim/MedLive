describe('Cadastro de Medico', () => {
    it('Deve preencher o formulário e retornar uma mensagem de sucesso', () => {
        cy.visit('http://localhost:3000/cadastro-medico')
        cy.get('input[name="nome"]').type('Dr. Carlos Souza')
        cy.get('input[name="email"]').type('carlos@gmail.com')
        cy.get('input[name="dataNascimento"]').type('1980-10-20')
        cy.get('input[name="genero"]').select('Masculino')
        cy.get('input[name="cpf"]').type('98765432100')
        cy.get('input[name="senha"]').type('senhaSegura123');
        cy.get('input[name="confirmarSenha"]').type('senhaSegura123')
        cy.get('input[name="crm"]').type('123456')
        cy.get('input[comprovante="file"]').attachFile('crm.pdf')
        cy.get('input[statusProfissional="file"]').select('Ativo')
        cy.get('button[type="submit"]').click()
        cy.contains('Médico cadastrado com sucesso!').should('be.visible')
  })
});

