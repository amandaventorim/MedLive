describe('Cadastro de Medico', () => {
    it('Deve preencher o formulário e retornar uma mensagem de sucesso', () => {
        cy.visit("http://127.0.0.1:8000/cadastro_medico")
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

describe("Login medico", () => {
      it("Deve fazer login com sucesso e redirecionar para a página inicial", () => {
        cy.visit("http://127.0.0.1:8000/login")
        cy.get('input[name="email"]').type("carlos@gmail.com")
        cy.get('input[name="senha"]').type("senhaSegura123")
     })
})


