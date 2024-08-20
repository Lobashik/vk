Для запуска приложения необходимо:
1) Запустить docker desktop
2) Открыть терминал и перейти в директорию, где лежит docker-compose.yml
3) Запустить docker compose командой:
    docker-compose up --build
4) Открыть в браузере страницу http://127.0.0.1:8000/api/schema/swagger-ui
На этой странице описание API в формате OpenAPI 3.0 (swagger-ui)
В приложении реализована аутентификация через JWT. Нужно отправлять в каждом запросе в заголовке Authorization Bearer <acccessToken>. Получается токен путем обращения к эндпоинту api/register, либо api/login. Для обращения к api/login нужно быть зарегестрированным через api/register. Время действия access токена - 5 минут. Для того, чтобы его поменять, нужно отправить refresh токен на эндпоинт api/refresh.

Описание эндпоинтов API:
api/register/

Регистрирует пользователя в системе.

request:
{
    "username": "user",
    "password": "password",
    "email": "some@mail.ru"
}
responses:
{
  "access": "string",
  "refresh": "string"
}
status 200;

{
    "error": "error's text"
}
status 400;


api/login
request:
{
  "username": "user",
  "password": "password"
}

responses:
{
  "access": "string",
  "refresh": "string"
}
status 200

{
    "detail": "Invalid password"
}
status 401

{
    "detail": "Invalid username"
}
status 404


api/refresh
request:
{
    "refresh": "refreshToken"
}

responses:
{
    "access": "accessToken"
}
status 200

{
    "detail": "Invalid refresh token"
}
status 400

{
    "detail": "Refresh token is required"
}
status 401


api/get_book
request:
{
    "titles": [
        "book1", "book2"
    ]
}

responses:
{
  "data": {
    "book1": {
      "id": 0,
      "title": "string",
      "author": "string",
      "year": 0
    },
    "book2": {
      "id": 0,
      "title": "string",
      "author": "string",
      "year": 0
    }
  }
}
status 200

{
    'error': 'Invalid input, expected list of keys.'
}
status 400

{
    "error": "error"
}
status 400


api/new_book
request:
{
  "title": "book1",
  "author": "author1",
  "year": 1999
}

responses:
{
    'status': 'success'
}
status 200

{
    "error": "error"
}
status 400