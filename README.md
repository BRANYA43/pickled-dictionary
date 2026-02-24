# Setup for developers
1. Activate venv
    ```bash
    uv venv .venv
    ```
2. Install dependencies
    ```bash
    uv sync --active
    ```
3. Install pre-commit hooks
    ```bash
    pre-commit install --hook-type commit-msg --hook-type pre-push --hook-type pre-commit
    ```
4. Copy environments from `sample.env` and define them
    ```bash
    cp environments/sample.env .env
    ```

# Architecture
- src/
  - database/ - слой БД
    - migrations/ - миграции
    - models/ - ORM модели
    - repositories/ - репозитории для моделей
    - config.py - настройки БД

  - gui/ - слой UI
    - screens/ - экраны приложения
    - widgets/ - виджеты

  - providers/ - провайдеры для авто-перевода, получения транскрипции и озвучивания.
  - services/ - Бизнес логика приложения 
  - utils/
  - view_models/ - слой для связывания gui с бизнес-логикой
  - app.py
  - run.py - точка запуска
  - settings.py - настройки приложения