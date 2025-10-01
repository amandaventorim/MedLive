describe("cadastro paciente", () => {
     it("Deve preencher o formulário e retornar uma mensagem de sucesso", () => {
        cy.visit("http://localhost:3000/cadastro-paciente")
        cy.get('input[name="nome"]').type("João Silva")    
        cy.get('input[name="cpf"]').type("12345678900")    
        cy.get('input[name="email"]').type("joaosilva@gmail.com")    
        cy.get('input[name="senha"]').type("senhaSegura123")    
        cy.get('input[name="genero"]').select("Masculino")    
        cy.get('input[name="dataNascimento"]').type("1990-05-15")    
        cy.get('textarea[name="endereco"]').type("Rua das Flores, 123, São Paulo, SP")    
        cy.get('input[name="convenio"]').type("Unimed")    
        cy.get('button[type="submit"]').click()
        cy.contains("Paciente cadastrado com sucesso!").should("be.visible")
  })
});