class TestAccessTokenEndpoint:
    route = "/api/auth/token/"

    async def test_get_access_token_valid_credentials(
        self,
        async_test_client_with_db_access_and_db_user,
        user_data,
    ):
        ac = async_test_client_with_db_access_and_db_user
        data = {
            "username": user_data["username"],
            "password": user_data["password"],
            "grant_type": "password"
        }

        response = await ac.post(self.route, data=data)
        response_data = response.json()

        assert response.status_code == 200
        assert "access_token" in response_data
        assert response_data["token_type"] == "Bearer"

    async def test_get_access_token_no_credentials(
            self,
            async_test_client_with_db_access_and_db_user
    ):
        ac = async_test_client_with_db_access_and_db_user
        data = {}

        response = await ac.post(self.route, data=data)

        assert response.status_code == 422

    async def test_get_access_token_fake_credentials(
            self,
            async_test_client_with_db_access_and_db_user
    ):
        fake_data = {
            "username": "fake-user",
            "password": "some-random-password",
            "grant_type": "password"
        }
        ac = async_test_client_with_db_access_and_db_user

        response = await ac.post(self.route, data=fake_data)
        response_data = response.json()

        assert response.status_code == 401
        assert response_data == {"detail": "Incorrect username or password"}

    async def test_get_access_token_invalid_password(
            self,
            async_test_client_with_db_access_and_db_user,
            user_data
    ):
        ac = async_test_client_with_db_access_and_db_user
        data = {
            "username": user_data["username"],
            "password": "invalid-password",
            "grant_type": "password"
        }

        response = await ac.post(self.route, data=data)
        response_data = response.json()

        assert response.status_code == 401
        assert response_data == {"detail": "Incorrect username or password"}
