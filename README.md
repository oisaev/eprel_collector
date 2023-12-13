
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)



## EPREL Collector

Сборщик информации, необходимой для генерации этикеток energy label из European Product Registry for Energy Labelling (EPREL).

### Стек технологий:
- Python 3.11
- Poetry
- asyncio
- aiohttp
- SQLAlchemy
- Alembic
- PostgreSQL

### Установка и запуск:
- Клонируйте репозиторий и перейдите в директорию проекта:
```
git clone git@github.com:oisaev/eprel_collector.git
```
```
cd eprel_collector/
```
- Создайте и заполните в ней файл **.env** - в качестве шаблона используйте файл **.env.example**
 - Инициализируйте создание директории виртуального окружения в проекте:

```
poetry config virtualenvs.in-project true
```

- Создайте директорию виртуального окружения:

```
poetry install
```
- Активируйте виртуальное окружение:
```
source .venv/bin/activate (для UNIX)
source .venv/Scripts/activate (для WINDOWS)
```
- Перейдите в директорию **eprel_collector/**
```
cd eprel_collector/
```
- Примените миграции для создания структуры БД:
```
alembic upgrade head
```
- Для получения информации по используемым аргументам командной строки, запустите проект с ключом **-h**:
```
python3 application.py -h (для UNIX)
python application.py -h (для WINDOWS)
```

© [Олег Исаев](https://github.com/oisaev), 2019-2023
