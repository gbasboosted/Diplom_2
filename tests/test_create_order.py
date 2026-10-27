import allure
import pytest


@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestCreateOrder:
    @allure.title("Создание заказа с ингредиентами")
    @pytest.mark.parametrize(
        "order_ingredients", [(0,), (0, 1, 2)],
        indirect=True, ids=["one-ingredient", "burger"],
    )
    def test_create_order_with_ingredients(self, api, order_ingredients, order_token):
        response = api.create_order({"ingredients": order_ingredients}, token=order_token)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert isinstance(body["name"], str) and body["name"]
        assert type(body["order"]["number"]) is int
        assert body["order"]["number"] > 0

    @allure.title("Создание заказа без ингредиентов: {payload}")
    @pytest.mark.parametrize("payload", [{"ingredients": []}, {}], ids=["empty-list", "missing-field"])
    def test_create_order_without_ingredients(self, api, order_token, payload):
        response = api.create_order(payload, token=order_token)

        assert response.status_code == 400
        assert response.json() == {"success": False, "message": "Ingredient ids must be provided"}

    @allure.title("Создание заказа с неверным 24-символьным хешем")
    def test_create_order_with_invalid_ingredient_hash(self, api, order_token):
        response = api.create_order(
            {"ingredients": ["61c0c5a71d1f82001bdaaa6z"]}, token=order_token
        )

        assert response.status_code == 500
        assert response.headers["Content-Type"].startswith("text/html")
        assert "<pre>Internal Server Error</pre>" in response.text
