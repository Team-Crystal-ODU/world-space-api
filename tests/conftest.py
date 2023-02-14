import pytest
from world_spc import create_app

# setup for test data, populating test db can go here


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        # DATABASE: db_path,
    })

    # call initialization functions here
    with app.app_context():
        #init_db()
        pass

    yield app

    #teardown 

# object to simulate client interaction with Flask app 
@pytest.fixture
def client(app):
    return app.test_client()

# potentially add fixture for test runner for cli here
