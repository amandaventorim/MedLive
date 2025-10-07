describe("cadastro paciente", () => {
     it("Deve preencher o formulário e retornar uma mensagem de sucesso", () => {
        cy.visit("http://127.0.0.1:8000/cadastro_paciente")
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

describe("Login paciente", () => {
     it("Deve fazer login com sucesso e redirecionar para a página inicial", () => {
        cy.visit("http://127.0.0.1:8000/login")
        cy.get('input[name="email"]').type("joao@gamil.com")
        cy.get('input[name="senha"]').type("senhaSegura123")
     })
})