function setUp() {
    // Add user
    cy.fixture('user').as('userJson').then(function (userJson) {
        cy.request({
            url: 'http://localhost:5000/users/create',
            form: true,
            body: userJson,
            method: 'POST'
        }).then((response) => {
            cy.writeFile('cypress/fixtures/userid.json', response.body)
            cy.wrap(response.body['_id']['$oid']).as('currentUserID');
        })
    })

    // Add task to user
    cy.fixture('tasks').as('tasksJson').then(function (taskJson) {
        cy.get('@currentUserID').then(currentUserID => {
            cy.request({
                url: 'http://localhost:5000/tasks/create',
                form: true,
                body: {
                    'title': taskJson.title,
                    'description': '(add a description here)',
                    'userid': currentUserID,
                    'url': taskJson.url,
                    'todos': 'Watch video'
                },
                method: 'POST'
            })
        })
    })
}

function loginAndOpenTask() {
    cy.visit('http://localhost:3000/')

    cy.get('h1').should('contain.text', 'Login')

    cy.contains('div', 'Email Address').find('input')
        .type('ampheris@gmail.com')

    // submit form
    cy.get('form').submit()

    // Assert that the user is logged in
    cy.get('h1')
        .should("contain.text", 'Your tasks, Mathilda Holmström')

    cy.get(".container-element a").click()
}

function tearDown() {
    cy.get('@currentUserID').then(currentUserID => {
        // Delete user
        cy.request({
            url: `http://localhost:5000/users/${currentUserID}`,
            method: 'DELETE'
        })
    })
}

describe('Users task testing', () => {
    beforeEach(() => {
        setUp()
        loginAndOpenTask()
    })

    afterEach(() => {
        tearDown()
    })

    // R8UC1 - USER ENTERS A DESCRIPTION
    it('should allow user to type in a description', () => {
        // Check that the description contains the correct value after type
        cy.get('.inline-form').find('input[type=text]').type('New todo')
            .should("contain.value", 'New todo')
    });

    // R8UC1 - PRESSES ADD BUTTON
    it('should allow the user to create new todo item when description is NOT empty', () => {
        // Check length of the list is +1 after form is submitted
        cy.get('.inline-form').find('input[type=text]').type('New todo')

        cy.get(".todo-list form").submit()

        cy.get(".todo-list .todo-item").should("have.length", 2)
    });

    it('should allow the user to create new todo item is at the bottom of the list', () => {
        // Check if the item is at the bottom of the list
    });

    it('should NOT allow the user to create new todo item when description is empty', () => {
        // Check so that the length is the same/expected value
        cy.get(".todo-list form").find('input[type=submit]').should('be.disabled')

        cy.get(".todo-list .todo-item").should("have.length", 1)
    });


    // R8UC2 - CLICKS ON ICON IN FRONT OF THE DESCRIPTION
    it('should make the todo item border red if its set to done', () => {
        // Check after a red border
    });

    it('should set active task to done if clicked', () => {
        // Check that the task is set to done
    });

    it('should done task should have its text struck through', () => {
        // Check that the tasks text is struck through
    });

    it('should set done task to active if clicked', () => {
        // Check so that the task is set to active
    });

    it('should remove the struck through text after task is set to active from done', () => {
        // Check if text is not struck through
    });


    // R8UC3 - CLICKS ON THE X SYMBOL BEHIND THE DESCRIPTION
    it('should remove todo from list if task is deleted', () => {
        // Check that the length of the list is -1 or the expected value.
        cy.get(".todo-list .todo-item").find('span[class=remover]').click().click()

        cy.get(".todo-list li").should("have.length", 1)
    });
})