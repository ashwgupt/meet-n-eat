import pytest
import os
import tempfile
from src.com.sep.demo import main
from src.com.sep.demo.users import usersOps
from src.com.sep.demo.requests import requestOps
from src.com.sep.demo.proposals import proposalOps

@pytest.fixture
def client(request):
    db_fileDescriptor, main.app.config['USER_DB'] = \
                                    tempfile.mkstemp()
    client = main.app.test_client()
    # with main.app.app_context():
    #     usersOps.initdb_command()
        # requestOps.initdb_command()
        # proposalOps.initdb_command()

    def teardown():
        """Get rid of the database again after each test."""
        os.close(db_fileDescriptor)
        os.unlink(main.app.config['USER_DB'])

    request.addfinalizer(teardown)
    return client


def add_user(client, user_name, user_password, user_email):
    received_response = client.post('/api/v1/users', data={
                "UserDetails": [
                    {"name": user_name,
                    "email": user_email,
                    "password": user_password}]
                },
                follow_redirects=True)
    return received_response


def test_users_retrieve(client):
    rcvd_resp = client.get('/api/v1/users')
    assert 'Your message was found' in rcvd_resp.data


def test_user_add(client):
    rcvd_resp = add_user(client,
                         "Ashwin Gupta",
                         "password",
                         "ashwin.gupta@abc.com")
    assert "User Created!!" in rcvd_resp.data