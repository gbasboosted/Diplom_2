# Расхождения API с документацией

## API-01: короткий неверный хеш возвращает 400 вместо описанного 500

Стенд: https://qa-stellarburgers.education-services.ru/.
Дата проверки: 26 октября 2026 года.

Запрос:

```http
POST /api/orders
Content-Type: application/json

{"ingredients": ["invalid-hash"]}
```

Воспроизведение без авторизации:

```bash
curl -i https://qa-stellarburgers.education-services.ru/api/orders \
  -H 'Content-Type: application/json' \
  -d '{"ingredients":["invalid-hash"]}'
```

Ожидаемый результат по
[предоставленной документации, страница 1](https://code.s3.yandex.net/qa-automation-engineer/python-full/diploma/Api-Stellar_Burgers.pdf):
HTTP 500 при невалидном хеше ингредиента.

Фактический результат: HTTP 400 и тело:

```json
{"success": false, "message": "One or more ids provided are incorrect"}
```

Расхождение воспроизводится с авторизацией и без неё — два параметризованных
тестовых случая. Для 24-символьного значения `61c0c5a71d1f82001bdaaa6z`
сервер возвращает ожидаемый HTTP 500.

Это расхождение контракта с документацией: API различает варианты невалидного
идентификатора, а документация описывает общий ответ 500. Ожидания в тестах
сохранены по документации; `skip`, `xfail` и принятие нескольких кодов не используются.
Нужно уточнить контракт и исправить документацию либо реализацию.
