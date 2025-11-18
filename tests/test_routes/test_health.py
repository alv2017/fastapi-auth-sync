class TestHealthEndpoint:
    async def test_health_check(self, async_test_client):
        ac = async_test_client

        response = await ac.get("/api/health/")
        response_data = response.json()

        assert response.status_code == 200
        assert "status" in response_data
        assert response_data["status"] == "OK"
