class TestWelcomeEndpoint:
    async def test_welcome_endpoint(self, async_test_client):
        ac = async_test_client

        response = await ac.get("/")
        response_data = response.json()

        assert response.status_code == 200
        assert "message" in response_data
        assert response_data["message"] == "Welcome!"