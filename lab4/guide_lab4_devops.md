# Лабораторная работа №4. Docker Compose

## 1. Что нужно сделать

По заданию нужно:

1. Изучить методические материалы по Docker Compose.
2. Взять выданный репозиторий проекта.
3. Создать `docker-compose.yml`.
4. Описать и поднять 3 сервиса:
   - `api`
   - `db`
   - `nginx`
5. Проверить, что сервисы работают и не уходят в перезапуск.

Исходные данные:

- PDF с методичкой: [lab4.pdf](/home/zevarch/Yandex.Disk/МТУСИ/dz_3pr/devops/lab4/lab4.pdf)
- Репозиторий проекта: [devops-lab4-main](/home/zevarch/Yandex.Disk/МТУСИ/dz_3pr/devops/lab4/devops-lab4-main)
- README проекта: [README.md](/home/zevarch/Yandex.Disk/МТУСИ/dz_3pr/devops/lab4/devops-lab4-main/README.md)

---

## 2. Краткая теория

### 2.1. Что такое Docker Compose

`Docker Compose` нужен для описания многоконтейнерного приложения в одном YAML-файле.

Обычно в `docker-compose.yml` описывают:

- сервисы
- сети
- тома
- переменные окружения
- проброс портов

После этого весь стек можно поднять одной командой:

```bash
docker compose up -d
```

### 2.2. Что такое сервис

Сервис в Compose - это описание контейнера:

- из какого образа запускать
- или из какой директории собирать образ
- какие порты открыть
- какие переменные окружения передать
- какие тома подключить
- к каким сетям подключить

### 2.3. Тома и bind mounts

Есть два похожих механизма:

- `volume` - управляется Docker
- `bind mount` - монтирует файл или папку с хоста

Примеры:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

Это именованный том.

```yaml
volumes:
  - ./nginx/dist:/public:ro
```

Это bind mount: папка `./nginx/dist` с хоста монтируется в контейнер по пути `/public`.

### 2.4. Сети

Сети позволяют контейнерам видеть друг друга по именам сервисов.

Если сервис `api` и сервис `db` находятся в одной сети, то backend может обращаться к БД по имени:

```text
db
```

То есть `DB_ADDR=db` работает именно потому, что контейнеры находятся в одной Docker-сети.

---

## 3. Что есть в проекте

Структура проекта:

```text
devops-lab4-main/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   └── src/
├── nginx/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── dist/
└── README.md
```

Что важно:

- `backend/Dockerfile` собирает Python API
- `backend/.env.example` показывает нужные переменные окружения
- `nginx/Dockerfile` собирает контейнер с nginx
- `nginx/nginx.conf` проксирует запросы `/api/v1` на сервис `api:8080`
- `nginx/dist/` содержит уже собранный фронтенд

---

## 4. Требования из README

По README нужно:

### Для `api`

- указать путь для сборки
- подключить сети `frontend` и `backend`
- пробросить порты
- передать переменные окружения через `backend/.env`

### Для `db`

- использовать образ `postgres`
- подключить сеть `backend`
- подключить том к `/var/lib/postgresql/data`
- задать `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`

### Для `nginx`

- указать путь для сборки
- подключить сеть `frontend`
- пробросить `80` порт
- смонтировать билд фронта в `/public`

---

## 5. Пошаговое выполнение

## 5.1. Переход в директорию проекта

```bash
cd /home/zevarch/Yandex.Disk/МТУСИ/dz_3pr/devops/lab4/devops-lab4-main
```

## 5.2. Создание файла `backend/.env`

Сначала нужно создать файл окружения для backend.

Содержимое:

```env
SERVER_ADDR=0.0.0.0
SERVER_PORT=8080
DB_ADDR=db
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432
DB_NAME=devopsLabs
```

Объяснение:

- `SERVER_ADDR=0.0.0.0` - backend слушает все интерфейсы внутри контейнера
- `SERVER_PORT=8080` - backend работает на 8080
- `DB_ADDR=db` - backend подключается к сервису `db` по имени контейнера в сети
- остальные переменные соответствуют настройкам PostgreSQL

Файл в проекте:

- [backend/.env](/home/zevarch/Yandex.Disk/МТУСИ/dz_3pr/devops/lab4/devops-lab4-main/backend/.env)

## 5.3. Создание `docker-compose.yml`

Рабочий файл:

- [docker-compose.yml](/home/zevarch/Yandex.Disk/МТУСИ/dz_3pr/devops/lab4/devops-lab4-main/docker-compose.yml)

Его содержимое:

```yaml
services:
  api:
    build:
      context: ./backend
    env_file:
      - ./backend/.env
    ports:
      - "8080:8080"
    networks:
      - frontend
      - backend
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: devopsLabs
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d devopsLabs"]
      interval: 5s
      timeout: 5s
      retries: 10
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

  nginx:
    build:
      context: ./nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx/dist:/public:ro
    networks:
      - frontend
    depends_on:
      - api

volumes:
  postgres_data:

networks:
  frontend:
  backend:
```

## 5.4. Разбор compose-файла

### Сервис `api`

```yaml
api:
  build:
    context: ./backend
```

Это значит, что образ собирается из директории `backend`.

```yaml
env_file:
  - ./backend/.env
```

Переменные окружения берутся из файла `backend/.env`.

```yaml
ports:
  - "8080:8080"
```

Порт `8080` хоста пробрасывается в `8080` контейнера.

```yaml
networks:
  - frontend
  - backend
```

`api` находится в двух сетях:

- в `backend`, чтобы видеть БД
- в `frontend`, чтобы его видел `nginx`

### Сервис `db`

```yaml
db:
  image: postgres:16
```

Берётся готовый официальный образ PostgreSQL.

```yaml
environment:
  POSTGRES_USER: postgres
  POSTGRES_PASSWORD: postgres
  POSTGRES_DB: devopsLabs
```

Так инициализируется база.

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

Данные PostgreSQL хранятся в именованном томе `postgres_data`, чтобы не потеряться после пересоздания контейнера.

```yaml
networks:
  - backend
```

База видна только внутри backend-сети.

### Сервис `nginx`

```yaml
nginx:
  build:
    context: ./nginx
```

Собирается из директории `nginx`.

```yaml
ports:
  - "80:80"
```

Снаружи приложение доступно на 80 порту.

```yaml
volumes:
  - ./nginx/dist:/public:ro
```

Статический фронтенд монтируется в `/public` только на чтение.

```yaml
networks:
  - frontend
```

`nginx` находится только во frontend-сети.

---

## 6. Проверка конфигурации

Перед запуском полезно проверить YAML:

```bash
docker compose config
```

Что делает команда:

- разворачивает итоговую конфигурацию
- показывает resolved-пути
- проверяет синтаксис
- проверяет ссылки на сети, тома и переменные

Если команда завершилась без ошибок, compose-файл корректный.

---

## 7. Сборка и запуск

## 7.1. Поднять стек

```bash
docker compose up -d --build
```

Разбор:

- `up` - создать и запустить сервисы
- `-d` - запуск в фоне
- `--build` - пересобрать образы перед стартом

## 7.2. Проверить состояние сервисов

```bash
docker compose ps
```

Ожидаемый результат:

- `api` в статусе `Up`
- `db` в статусе `Up (healthy)`
- `nginx` в статусе `Up`

Пример:

```text
NAME                       IMAGE                    COMMAND                  SERVICE   STATUS
devops-lab4-main-api-1     devops-lab4-main-api     "python main.py"         api       Up
devops-lab4-main-db-1      postgres:16              "docker-entrypoint..."   db        Up (healthy)
devops-lab4-main-nginx-1   devops-lab4-main-nginx   "./nginx/sbin/nginx"     nginx     Up
```

## 7.3. Посмотреть логи

```bash
docker compose logs --tail=50
```

На что смотреть:

- backend должен запуститься без traceback
- PostgreSQL должен выйти в состояние `ready to accept connections`
- у `nginx` не должно быть фатальных ошибок

Пример полезных строк:

```text
api-1  | INFO:     Application startup complete.
api-1  | INFO:     Uvicorn running on http://0.0.0.0:8080
db-1   | database system is ready to accept connections
```

---

## 8. Проверка доступности приложения

### 8.1. Проверка фронта через nginx

Открыть в браузере:

```text
http://localhost/
```

Так как `nginx` публикуется на порту 80, фронтенд должен открываться без указания порта.

### 8.2. Проверка API

Так как `nginx` проксирует `/api/v1` на backend, можно тестировать API через nginx.

Например:

```bash
curl http://localhost/api/v1
```

Или открыть доступные эндпоинты, если они предусмотрены приложением.

---

## 9. Почему здесь есть `depends_on` и `healthcheck`

Формально задание требует только описать 3 сервиса. Но на практике возникает проблема:

- `api` может стартовать раньше, чем PostgreSQL примет соединения
- тогда backend иногда падает на старте или уходит в ошибку

Чтобы запуск был устойчивым, добавлены:

```yaml
depends_on:
  db:
    condition: service_healthy
```

и

```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U postgres -d devopsLabs"]
```

Это не противоречит заданию. Это просто нормальная практическая доработка, чтобы стек стабильно поднимался.

---

## 10. Типичные ошибки

## 10.1. Ошибка с `postgres_data`

Ошибка из контрольного вопроса связана с тем, что запись:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

воспринимается как именованный том, а не как локальная папка.

Если хотели именно папку проекта, нужно писать:

```yaml
volumes:
  - ./postgres_data:/var/lib/postgresql/data
```

Если хотели именно Docker volume, его нужно объявить внизу:

```yaml
volumes:
  postgres_data:
```

## 10.2. Backend не видит БД

Проверь:

- что `api` и `db` находятся в одной сети `backend`
- что в `.env` указано `DB_ADDR=db`
- что `POSTGRES_*` совпадают с `DB_*`

## 10.3. Nginx не видит API

Проверь:

- что `nginx` и `api` находятся в сети `frontend`
- что в `nginx.conf` прокси настроен на `http://api:8080`

## 10.4. Контейнеры постоянно перезапускаются

Смотри:

```bash
docker compose ps
docker compose logs --tail=100
```

Если `db` долго стартует, а `api` подключается к ней слишком рано, обычно помогает `healthcheck` и зависимость от `service_healthy`.

---

## 11. Основные команды Docker Compose для защиты

Поднять стек:

```bash
docker compose up -d --build
```

Остановить и удалить контейнеры:

```bash
docker compose down
```

Остановить и удалить контейнеры вместе с томами:

```bash
docker compose down -v
```

Показать состояние:

```bash
docker compose ps
```

Показать логи:

```bash
docker compose logs
```

Показать итоговую конфигурацию:

```bash
docker compose config
```

---

## 12. Что можно говорить на защите

Короткая логика работы проекта:

1. `db` поднимает PostgreSQL и хранит данные в Docker volume.
2. `api` запускает Python backend и подключается к БД по имени `db`.
3. `nginx` раздаёт статический фронтенд из `/public`.
4. Запросы на `/api/v1` nginx проксирует на backend `api:8080`.

Почему 2 сети:

- `backend` нужна для связи `api <-> db`
- `frontend` нужна для связи `nginx <-> api`

Почему нужен том:

- без тома данные PostgreSQL пропадут после удаления контейнера

Почему bind mount для фронта:

- потому что нужно подмонтировать готовый билд с хоста в `/public`

---

## 13. Ответы на контрольные вопросы

### 13.1. Что такое Docker Compose и для чего он используется

Docker Compose - это инструмент для определения и запуска многоконтейнерных приложений.

Он используется, чтобы:

- описать несколько сервисов в одном файле
- настроить между ними сети
- подключить тома
- задать переменные окружения
- запускать весь стек одной командой

### 13.2. Почему возникает ошибка при монтировании `postgres_data`

Потому что запись `postgres_data:/var/lib/postgresql/data` без `./` воспринимается как именованный том, а не как директория на хосте.

Исправления:

- либо объявить именованный том:

```yaml
volumes:
  postgres_data:
```

- либо явно указать локальную папку:

```yaml
volumes:
  - ./postgres_data:/var/lib/postgresql/data
```

---

## 14. Итог

В этой лабораторной нужно не просто знать синтаксис YAML, а понимать взаимодействие сервисов:

- кто с кем общается
- через какие сети
- где хранятся данные
- какие переменные окружения нужны приложению

Итоговая рабочая конфигурация для этой лабы уже подготовлена:

- [docker-compose.yml](/home/zevarch/Yandex.Disk/МТУСИ/dz_3pr/devops/lab4/devops-lab4-main/docker-compose.yml)
- [backend/.env](/home/zevarch/Yandex.Disk/МТУСИ/dz_3pr/devops/lab4/devops-lab4-main/backend/.env)
- [report_lab4_devops.docx](/home/zevarch/Yandex.Disk/МТУСИ/dz_3pr/devops/lab4/report_lab4_devops.docx)

Если нужен короткий вариант под сдачу, можно брать разделы `5`, `7`, `10` и `13`.
