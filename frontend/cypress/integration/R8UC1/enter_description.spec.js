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
        })
    })

    // Add task to user
    cy.fixture('tasks').as('tasksJson').then(function (taskJson) {
        cy.fixture('userid').as('useridJson').then(function (useridJson) {
            cy.request({
                url: 'http://localhost:5000/tasks/create',
                form: true,
                body: {
                    'title': taskJson.title,
                    'description': '(add a description here)',
                    'userid': useridJson['_id']['$oid'],
                    'url': taskJson.url,
                    'todos': 'Watch video'
                },
                method: 'POST'
            })
        })
    })

    // Go to website
    cy.visit('http://localhost:3000/')
}

function loginAndOpenTask() {
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
    // Delete user
    cy.fixture('userid').as('useridJson').then(function (useridJson) {
        cy.request({
            url: `http://localhost:5000/users/${useridJson['_id']['$oid']}`,
            method: 'DELETE'
        })
    })
}

describe('User enters a new tasks description', () => {
    before(() => {
        setUp()
        loginAndOpenTask()
    })

    after(() => {
        tearDown()
    })

    it('should open up the test task', function () {

    });

})