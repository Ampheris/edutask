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

    // Log in
    cy.fixture('user').as('userJson').then(function (userJson) {
        cy.request('GET', `http://localhost:5000/users/bymail/${userJson.email}`)
    })
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
    beforeEach(() => {
        setUp()
    })

    afterEach(() => {
        tearDown()
    })

    it('should allow user to type in a description', function () {
        cy.wait(1000)
        /*cy.get('input').find('[type="text"]').type('test test')
            .next().should('contain', 'test test')*/
    });
})