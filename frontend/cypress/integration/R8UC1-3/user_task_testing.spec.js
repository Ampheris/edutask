function setUp() {
    let userID = '';

    // Add user
    cy.fixture('user').as('userJson').then(function (userJson) {
        cy.request({
            url: 'http://localhost:5000/users/create',
            form: true,
            body: userJson,
            method: 'POST'
        }).then((response) => {
            cy.writeFile('cypress/fixtures/userid.json', response.body)
        })
    })

    cy.readFile('cypress/fixtures/userid.json').then((userObject) => {
        userID = userObject['_id']['$oid'];
    });

    // Add task to user
    cy.fixture('tasks').as('tasksJson').then(function (taskJson) {
        cy.request({
            url: 'http://localhost:5000/tasks/create',
            form: true,
            body: {
                'title': taskJson.title,
                'description': '(add a description here)',
                'userid': userID,
                'url': taskJson.url,
                'todos': 'Watch video'
            },
            method: 'POST'
        })
    })
}

function loginAndOpenTask() {
    // Go to website
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
    let userID = '';

    cy.readFile('cypress/fixtures/userid.json').then((userObject) => {
        userID = userObject['_id']['$oid'];
    });

    cy.fixture('userid').as('useridJson').then(function () {
        // Delete user
        cy.request({
            url: `http://localhost:5000/users/${userID}`,
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

        cy.get('.inline-form').find('input[type=text]').clear()
    });

    // R8UC1 - PRESSES ADD BUTTON
    it('should allow the user to create new todo item when description is NOT empty', () => {
        // Check length of the list is +1 after form is submitted
        cy.get('.inline-form').find('input[type=text]').type('New todo')

        cy.get(".todo-list form").submit()

        cy.get(".todo-list .todo-item").should(($todoList) => {
            expect($todoList).to.have.length(2);
        })
    });

    /* it('should allow the user to create new todo item is at the bottom of the list', () => {
         // Check if the item is at the bottom of the list
     });

     it('should NOT allow the user to create new todo item when description is empty', () => {
         // Check so that the length is the same/expected value
         cy.get('.inline-form').find('input[type=text]').clear()

         cy.get(".todo-list form").submit()

         cy.get(".todo-list .todo-item").should(($todoList) => {
             expect($todoList).to.have.length(1);
         })
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
     });*/
})