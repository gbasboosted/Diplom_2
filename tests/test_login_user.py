import allure
import pytest


@allure.epic("Stellar Burgers API")
@allure.feature("Логин пользователя")
class TestLoginUser:
    @allure.title("Вход существующего пользователя")
    def test_login_existing_user(self, api, registered_user):
        data = registered_user["data"]
        response = api.login({"email": data["email"], "password": data["password"]})

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"] == {"email": data["email"], "name": data["name"]}
        assert body["accessToken"].startswith("Bearer ")
        assert len(body["accessToken"]) > len("Bearer ")
        assert isinstance(body["refreshToken"], str) and body["refreshToken"]

    @allure.title("Вход с неверными данными")
    @pytest.mark.parametrize(
        "invalid_credentials",
        [("invalid", "valid"), ("valid", "invalid"), ("invalid", "invalid")],
        indirect=True, ids=["email", "password", "both"],
    )
    def test_login_with_invalid_credentials(self, api, invalid_credentials):
        response = api.login(invalid_credentials)

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": "email or password are incorrect"}
