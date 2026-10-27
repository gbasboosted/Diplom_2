import allure
import pytest


@allure.epic("Stellar Burgers API")
@allure.feature("Создание пользователя")
class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, register_user, user_data):
        response = register_user(user_data)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"] == {"email": user_data["email"], "name": user_data["name"]}
        assert body["accessToken"].startswith("Bearer ")
        assert len(body["accessToken"]) > len("Bearer ")
        assert isinstance(body["refreshToken"], str) and body["refreshToken"]

    @allure.title("Повторная регистрация существующего пользователя")
    def test_create_existing_user(self, register_user, registered_user):
        response = register_user(registered_user["data"])

        assert response.status_code == 403
        assert response.json() == {"success": False, "message": "User already exists"}

    @allure.title("Регистрация с отсутствующим или пустым обязательным полем")
    @pytest.mark.parametrize(
        "registration_payload",
        [
            pytest.param((("password", "name"), {}), id="missing-email"),
            pytest.param((("email", "name"), {}), id="missing-password"),
            pytest.param((("email", "password"), {}), id="missing-name"),
            pytest.param((("email", "password", "name"), {"email": ""}), id="empty-email"),
            pytest.param((("email", "password", "name"), {"password": ""}), id="empty-password"),
            pytest.param((("email", "password", "name"), {"name": ""}), id="empty-name"),
        ],
        indirect=True,
    )
    def test_create_user_without_required_field(self, register_user, registration_payload):
        response = register_user(registration_payload)

        assert response.status_code == 403
        assert response.json() == {
            "success": False, "message": "Email, password and name are required fields",
        }
