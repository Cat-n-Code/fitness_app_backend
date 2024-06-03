
## Установка и запуск
1. Убедитесь, что у вас установлен [Docker](https://www.docker.com/)
2. Склонируйте данный репозиторий:
    ```shell
    git clone https://github.com/Cat-n-Code/fitness_app_backend.git && cd fitness_app_backend
    ```
2. Создайте `.env` файл с конфигурацией сервиса. Ниже приведен пример файла:
    ```text
    SERVER_PORT=8080
    AUTH_TOKEN_SECRET_KEY=I5DrSPTUuY8ytohMTC3nwnRLqsbLZHNYn9zufr49mG0=
    INITIAL_USER=null
    DB_URL=postgresql+psycopg://user:qwerty12@database:5432/fitness_app

    POSTGRES_DATABASE=fitness_app
    POSTGRES_USER=user
    POSTGRES_PASSWORD=qwerty12
    ```
3. Запустите сервис:
    ```shell
    docker compose up -d
    ```
4. После запуска, сервис будет доступен по адресу http://localhost:8080. Также
    по адресу http://localhost:8080/docs будет доступна OpenAPI документация.
5. Остановка сервиса:
    ```shell
    docker compose down
    ```
