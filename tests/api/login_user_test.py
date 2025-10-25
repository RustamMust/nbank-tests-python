import pytest
import requests


@pytest.mark.api
class TestLoginUser:
    @pytest.mark.debug
    @pytest.mark.parametrize(
            'username, password, role',
            [('login_user123', 'verysTRongPassword33$', 'USER')]
    )
    def test_login_user(self, username: str, password: str, role: str):
        # create user
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
        print(login_response.headers.get('authorization'))

    def test_login_admin_user(self):
        login_response = requests.post(
            url='http://localhost:4111/api/v1/auth/login',
            json={
                "username": 'admin',
                "password": 'admin'
            },
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        )

        assert login_response.status_code == 200
        assert login_response.headers.get('authorization') == 'Basic YWRtaW46YWRtaW4='
