describe("Todo Tests", () => {

    beforeEach(() => {
        cy.visit("http://localhost:3000")

        cy.contains("Click here to sign up").click()

        const email = "test" + Date.now() + Math.floor(Math.random() * 1000) + "@example.com"

        cy.get("input").eq(0).clear().type(email)
        cy.get("input").eq(1).clear().type("Test")
        cy.get("input").eq(2).clear().type("User")

        cy.contains("Sign Up").click()

        cy.contains("Your tasks").should("exist")
    })

    function createTask(title) {
        cy.intercept("POST", "**/tasks/create").as("createTask")

        cy.get('input[placeholder="Title of your Task"]')
            .clear()
            .type(title)

        cy.get('input[placeholder*="Viewkey"]')
            .clear()
            .type("Ijy7MOzG8Fo")

        cy.contains("Create new Task").click()

        cy.wait("@createTask")
            .its("response.statusCode")
            .should("eq", 200)

        cy.contains(title)
            .should("exist")
            .click()

        cy.contains("Watch video")
            .should("exist")
    }

    function addTodo(todoText) {
        cy.intercept("POST", "**/todos/create").as("createTodo")

        cy.get('input[placeholder="Add a new todo item"]')
            .clear()
            .type(todoText)

        cy.contains("Add").click()

        cy.wait("@createTodo")
            .its("response.statusCode")
            .should("eq", 200)

        cy.contains(todoText)
            .should("exist")
    }

    it("R8UC1 - should add a todo item", () => {
        createTask("Learn Cypress")

        addTodo("Read documentation")

        cy.contains("Read documentation")
            .should("exist")
    })

    it("R8UC2 - should toggle a todo item", () => {
        createTask("Toggle Task")

        cy.contains("Watch video")
            .should("exist")

        cy.contains("Watch video")
            .closest("li.todo-item")
            .click("left", { force: true })

        cy.contains("Watch video")
            .should("exist")
    })

    it("R8UC3 - should delete a todo item", () => {
        createTask("Delete Task")

        addTodo("Delete me")

        cy.intercept("DELETE", "**/todos/byid/**").as("deleteTodo")

        cy.contains("Delete me")
            .closest("li.todo-item")
            .find("span.remover")
            .click({ force: true })

        cy.wait("@deleteTodo")
            .its("response.statusCode")
            .should("eq", 200)
    })

})