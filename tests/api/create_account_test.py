import pytest
import requests


@pytest.mark.api
class TestCreateAccount:
    @pytest.mark.parametrize(
            'username, password, role',
            [('createaccount1', 'verysTRongPassword33$', 'USER')]
    )
    def test_create_account(self, username: str, password: str, role: str):
        create_user_response = requests.post(
            url='http://localhost:4111/api/v1/admin/users',
            json={
                "username": username,
                "password": password,
                "role": role
            },
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': 'Basic YWRtaW46YWRtaW4='
            }
        )

        assert create_user_response.status_code == 201

        login_response = requests.post(
            url='http://localhost:4111/api/v1/auth/login',
            json={
                "username": username,
                "password": password
            },
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )

        assert login_response.status_code == 200
        assert login_response.headers.get('authorization')

        create_account_response = requests.post(
            url='http://localhost:4111/api/v1/accounts',
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': login_response.headers.get('authorization')
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get('balance') == 0.0
        assert not create_account_response.json().get('transactions')
