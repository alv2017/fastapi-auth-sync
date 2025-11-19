import pytest

empty_user_data_params = [
    ("empty_string", ""),
    ("whitespaces", "   "),
    ("null_value", None),
    ("error_type", {}),
    ("error_type", []),
]


class TestUsersRegistrationEndpoint:
    route = "/api/users/register/"

    async def test_register_user_success(
        self, async_test_client_with_db_access, user_data
    ):
        ac = async_test_client_with_db_access

        response = await ac.post(self.route, json=user_data)
        response_data = response.json()

        assert response.status_code == 201
        assert bool(response_data)
        assert "id" in response_data
        assert response_data["username"] == user_data["username"]
        assert response_data["email"] == user_data["email"]

    async def test_register_user_conflict(
        self, async_test_client_with_db_access, user_data
    ):
        ac = async_test_client_with_db_access

        # first registration should succeed
        response = await ac.post(self.route, json=user_data)
        assert response.status_code == 201

        # second registration with same data should fail
        response = await ac.post(self.route, json=user_data)
        response_data = response.json()

        assert response.status_code == 409
        assert response_data == {
            "detail": "User with provided username or email already exists"
        }

    @pytest.mark.parametrize("error_type,error_value", empty_user_data_params)
    async def test_register_with_invalid_data_empty(
        self,
        error_type,
        error_value,
        async_test_client_with_db_access,
    ):
        ac = async_test_client_with_db_access
        invalid_user_data = error_value

        response = await ac.post(self.route, json=invalid_user_data)
        assert response.status_code == 422

    async def test_register_with_invalid_data_missing_username(
        self, async_test_client_with_db_access
    ):
        ac = async_test_client_with_db_access
        invalid_user_data = {
            "email": "test-user@example.com",
            "password": "Strong-Unbreakable-Password-07",
        }
        response = await ac.post(self.route, json=invalid_user_data)
        assert response.status_code == 422

    async def test_register_with_invalid_data_missing_email(
        self, async_test_client_with_db_access
    ):
        ac = async_test_client_with_db_access
        invalid_user_data = {
            "username": "test-user",
            "password": "Strong-Unbreakable-Password-07",
        }
        response = await ac.post(self.route, json=invalid_user_data)
        assert response.status_code == 422

    async def test_register_with_invalid_data_missing_password(
        self, async_test_client_with_db_access
    ):
        ac = async_test_client_with_db_access
        invalid_user_data = {"username": "test-user", "email": "test-user@example.com"}
        response = await ac.post(self.route, json=invalid_user_data)
        assert response.status_code == 422

    async def test_register_with_invalid_data_username_too_short(
        self, async_test_client_with_db_access
    ):
        ac = async_test_client_with_db_access
        invalid_user_data = {
            "username": "tu",
            "email": "test-user@example.com",
            "password": "Strong-Unbreakable-Password-07",
        }
        response = await ac.post(self.route, json=invalid_user_data)
        assert response.status_code == 422


class TestGetUserMeEndpoint:
    route = "/api/users/me/"

    async def test_get_user_me_no_token(self, async_test_client_with_db_access):
        ac = async_test_client_with_db_access

        response = await ac.get(self.route)
        response_data = response.json()

        assert response.status_code == 401
        assert response_data == {"detail": "Not authenticated"}

    async def test_get_user_me_valid_token(self, async_authorized_test_client):
        ac = async_authorized_test_client

        response = await ac.get(self.route)
        response_data = response.json()

        assert response.status_code == 200
        assert "id" in response_data
        assert "username" in response_data
        assert "email" in response_data

    async def test_get_user_me_expired_token(
        self, async_test_client_with_expired_token
    ):
        ac = async_test_client_with_expired_token

        response = await ac.get(self.route)
        response_data = response.json()

        assert response.status_code == 403
        assert response_data == {"detail": "Access Forbidden: Token has expired"}

    async def test_get_user_me_faked_token(self, async_test_client_with_faked_token):
        ac = async_test_client_with_faked_token

        response = await ac.get(self.route)
        response_data = response.json()

        assert response.status_code == 403
        assert "Access Forbidden: Invalid token" in response_data["detail"]

    async def test_get_user_me_invalid_token(
        self, async_test_client_with_invalid_token
    ):
        ac = async_test_client_with_invalid_token

        response = await ac.get(self.route)
        response_data = response.json()

        assert response.status_code == 403
        assert "Access Forbidden: Invalid token" in response_data["detail"]
