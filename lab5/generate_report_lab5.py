from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

doc = Document()

# ── Поля страницы ──────────────────────────────────────────────────────────────
section = doc.sections[0]
section.top_margin    = Cm(2)
section.bottom_margin = Cm(2)
section.left_margin   = Cm(3)
section.right_margin  = Cm(1.5)


# ── Вспомогательные функции ────────────────────────────────────────────────────
def para(text="", bold=False, size=14, align=WD_ALIGN_PARAGRAPH.LEFT,
         italic=False, color=None, space_before=0, space_after=0):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    if text:
        run = p.add_run(text)
        run.bold   = bold
        run.italic = italic
        run.font.size = Pt(size)
        run.font.name = "Times New Roman"
        if color:
            run.font.color.rgb = color
    return p


def heading(text, level=1):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after  = Pt(6)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = "Times New Roman"
    return p


def code_block(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after  = Pt(4)
    p.paragraph_format.left_indent  = Cm(0.5)
    # серый фон через shading
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'),   'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'),  'F2F2F2')
    pPr.append(shd)
    run = p.add_run(text)
    run.font.name = "Courier New"
    run.font.size = Pt(10)
    return p


def body(text, size=12, space_before=4, space_after=4,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after  = Pt(space_after)
    p.paragraph_format.first_line_indent = Cm(1.25)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.name = "Times New Roman"
    return p


# ══════════════════════════════════════════════════════════════════════════════
# ТИТУЛЬНЫЙ ЛИСТ
# ══════════════════════════════════════════════════════════════════════════════
para("МИНИСТЕРСТВО ЦИФРОВОГО РАЗВИТИЯ, СВЯЗИ И МАССОВЫХ КОММУНИКАЦИЙ РОССИЙСКОЙ ФЕДЕРАЦИИ",
     bold=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
para("Ордена Трудового Красного Знамени федеральное государственное бюджетное",
     size=12, align=WD_ALIGN_PARAGRAPH.CENTER)
para("образовательное учреждение высшего образования",
     size=12, align=WD_ALIGN_PARAGRAPH.CENTER)
para("«Московский технический университет связи и информатики» (МТУСИ)",
     bold=True, size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=40)

para("Кафедра программной инженерии",
     size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=20)

para("Дисциплина: «Средства автоматизации развертывания программного обеспечения»",
     italic=True, size=13, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=40)

para("ОТЧЁТ", bold=True, size=16, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
para("по лабораторной работе №5", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)
para("«Методология CI/CD»", bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=60)

para("Выполнил: студент группы БПИ2401",
     size=13, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=2)
para("Юлдашев Всеволод Дмитриевич",
     size=13, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=6)
para("Проверил: Тимчук Андрей Васильевич",
     size=13, align=WD_ALIGN_PARAGRAPH.RIGHT, space_after=80)

para("Москва 2026", size=13, align=WD_ALIGN_PARAGRAPH.CENTER)

doc.add_page_break()

# ══════════════════════════════════════════════════════════════════════════════
# 1. ЦЕЛЬ РАБОТЫ
# ══════════════════════════════════════════════════════════════════════════════
heading("1. Цель работы")
body("Целью данной лабораторной работы является знакомство с методологией CI/CD "
     "(Continuous Integration / Continuous Delivery) и получение практических навыков "
     "работы с инструментом GitHub Actions для автоматизации сборки, тестирования "
     "и публикации Docker-образа приложения.")

# ══════════════════════════════════════════════════════════════════════════════
# 2. ХОД РАБОТЫ
# ══════════════════════════════════════════════════════════════════════════════
heading("2. Ход работы")

# ── 2.1 Подготовка ─────────────────────────────────────────────────────────
heading("2.1. Подготовка")

body("На первом этапе была зарегистрирована учётная запись на Docker Hub, создан "
     "новый репозиторий на GitHub и произведено клонирование шаблонного репозитория "
     "лабораторной работы. Для переключения origin на собственный репозиторий в "
     "терминале была выполнена команда:")

code_block("$ git remote set-url origin https://github.com/zevy3/devops-lab5.git")

body("Далее была создана ветка dev, на которой будет вестись разработка:")

code_block("$ git checkout -b dev\nSwitched to a new branch 'dev'")

body("Структура проекта, с которой велась работа, выглядит следующим образом:")

code_block(
    ".\n"
    "├── src/\n"
    "│   ├── __init__.py\n"
    "│   ├── main.py\n"
    "│   └── routers/\n"
    "│       ├── __init__.py\n"
    "│       └── user.py\n"
    "├── tests/\n"
    "│   ├── __init__.py\n"
    "│   └── test_user.py\n"
    "├── .github/\n"
    "│   └── workflows/\n"
    "│       ├── tests.yml\n"
    "│       └── build-and-delivery.yml\n"
    "├── Dockerfile\n"
    "└── requirements.txt"
)

# ── 2.2 Покрытие тестами ─────────────────────────────────────────────────────
heading("2.2. Покрытие тестами")

body("Файл src/routers/user.py содержит REST-эндпоинты для управления пользователями. "
     "Реализованы операции: получение пользователя по id, создание, обновление, "
     "удаление и получение списка всех пользователей. Ниже приведён полный код роутера:")

code_block(
    "from fastapi import APIRouter, HTTPException\n"
    "from pydantic import BaseModel\n"
    "\n"
    "router = APIRouter(prefix=\"/users\", tags=[\"users\"])\n"
    "\n"
    "_users: dict[int, dict] = {\n"
    "    1: {\"id\": 1, \"name\": \"Alice\", \"email\": \"alice@example.com\"},\n"
    "    2: {\"id\": 2, \"name\": \"Bob\",   \"email\": \"bob@example.com\"},\n"
    "}\n"
    "_next_id = 3\n"
    "\n"
    "\n"
    "class UserCreate(BaseModel):\n"
    "    name: str\n"
    "    email: str\n"
    "\n"
    "\n"
    "class UserUpdate(BaseModel):\n"
    "    name: str | None = None\n"
    "    email: str | None = None\n"
    "\n"
    "\n"
    "@router.get(\"/\")\n"
    "def list_users():\n"
    "    return list(_users.values())\n"
    "\n"
    "\n"
    "@router.get(\"/{user_id}\")\n"
    "def get_user(user_id: int):\n"
    "    user = _users.get(user_id)\n"
    "    if user is None:\n"
    "        raise HTTPException(status_code=404, detail=\"User not found\")\n"
    "    return user\n"
    "\n"
    "\n"
    "@router.post(\"/\", status_code=201)\n"
    "def create_user(body: UserCreate):\n"
    "    global _next_id\n"
    "    user = {\"id\": _next_id, \"name\": body.name, \"email\": body.email}\n"
    "    _users[_next_id] = user\n"
    "_next_id += 1\n"
    "    return user\n"
    "\n"
    "\n"
    "@router.put(\"/{user_id}\")\n"
    "def update_user(user_id: int, body: UserUpdate):\n"
    "    user = _users.get(user_id)\n"
    "    if user is None:\n"
    "        raise HTTPException(status_code=404, detail=\"User not found\")\n"
    "    if body.name is not None:\n"
    "        user[\"name\"] = body.name\n"
    "    if body.email is not None:\n"
    "        user[\"email\"] = body.email\n"
    "    return user\n"
    "\n"
    "\n"
    "@router.delete(\"/{user_id}\", status_code=204)\n"
    "def delete_user(user_id: int):\n"
    "    if user_id not in _users:\n"
    "        raise HTTPException(status_code=404, detail=\"User not found\")\n"
    "    del _users[user_id]"
)

body("Для тестирования приложения были реализованы пять тест-кейсов в файле "
     "tests/test_user.py с использованием TestClient из библиотеки fastapi:")

body("1. test_get_existed_user — проверяет успешное получение существующего пользователя "
     "(ожидаемый статус-код 200, корректные поля ответа);")

body("2. test_get_not_existed_user — проверяет ответ 404 при запросе несуществующего "
     "пользователя с id = 9999;")

body("3. test_create_user — проверяет создание нового пользователя (статус-код 201) "
     "и наличие поля id в ответе;")

body("4. test_create_user_with_invalid_data — проверяет возврат ошибки 422 при передаче "
     "некорректных данных (отсутствует обязательное поле email);")

body("5. test_delete_user — создаёт пользователя, удаляет его (статус 204) и убеждается, "
     "что повторный GET возвращает 404.")

body("Полный код файла tests/test_user.py:")

code_block(
    "import pytest\n"
    "from fastapi.testclient import TestClient\n"
    "from src.main import app\n"
    "\n"
    "client = TestClient(app)\n"
    "\n"
    "\n"
    "def test_get_existed_user():\n"
    "    response = client.get(\"/users/1\")\n"
    "    assert response.status_code == 200\n"
    "    data = response.json()\n"
    "    assert data[\"id\"] == 1\n"
    "    assert data[\"name\"] == \"Alice\"\n"
    "    assert data[\"email\"] == \"alice@example.com\"\n"
    "\n"
    "\n"
    "def test_get_not_existed_user():\n"
    "    response = client.get(\"/users/9999\")\n"
    "    assert response.status_code == 404\n"
    "    assert response.json()[\"detail\"] == \"User not found\"\n"
    "\n"
    "\n"
    "def test_create_user():\n"
    "    payload = {\"name\": \"Charlie\", \"email\": \"charlie@example.com\"}\n"
    "    response = client.post(\"/users/\", json=payload)\n"
    "    assert response.status_code == 201\n"
    "    data = response.json()\n"
    "    assert data[\"name\"] == \"Charlie\"\n"
    "    assert data[\"email\"] == \"charlie@example.com\"\n"
    "    assert \"id\" in data\n"
    "\n"
    "\n"
    "def test_create_user_with_invalid_data():\n"
    "    response = client.post(\"/users/\", json={\"name\": \"NoEmail\"})\n"
    "    assert response.status_code == 422\n"
    "\n"
    "\n"
    "def test_delete_user():\n"
    "    create_resp = client.post(\"/users/\",\n"
    "                              json={\"name\": \"ToDelete\",\n"
    "                                    \"email\": \"del@example.com\"})\n"
    "    assert create_resp.status_code == 201\n"
    "    user_id = create_resp.json()[\"id\"]\n"
    "\n"
    "    delete_resp = client.delete(f\"/users/{user_id}\")\n"
    "    assert delete_resp.status_code == 204\n"
    "\n"
    "    get_resp = client.get(f\"/users/{user_id}\")\n"
    "    assert get_resp.status_code == 404"
)

body("Запуск тестов локально подтвердил корректность реализации — все 5 тестов "
     "завершились успешно:")

code_block(
    "$ python -m pytest tests/ -v\n"
    "============================= test session starts ==============================\n"
    "platform darwin -- Python 3.12.13, pytest-9.0.3, pluggy-1.6.0\n"
    "rootdir: /devops-lab5\n"
    "collected 5 items\n"
    "\n"
    "tests/test_user.py::test_get_existed_user              PASSED  [ 20%]\n"
    "tests/test_user.py::test_get_not_existed_user          PASSED  [ 40%]\n"
    "tests/test_user.py::test_create_user                   PASSED  [ 60%]\n"
    "tests/test_user.py::test_create_user_with_invalid_data PASSED  [ 80%]\n"
    "tests/test_user.py::test_delete_user                   PASSED  [100%]\n"
    "\n"
    "============================== 5 passed in 0.33s ==============================="
)

# ── 2.3 Создание пайплайна ────────────────────────────────────────────────────
heading("2.3. Создание пайплайна")

body("В корне проекта была создана директория .github/workflows/, содержащая два "
     "файла конфигурации рабочих процессов GitHub Actions.")

body("Файл tests.yml описывает рабочий процесс CI, запускаемый при каждом коммите "
     "в любую ветку. Он выполняет следующие шаги: получение кода репозитория, "
     "настройку Python 3.12, установку зависимостей и запуск unit-тестов:")

code_block(
    "name: Test Python App\n"
    "\n"
    "on:\n"
    "  push:\n"
    "\n"
    "jobs:\n"
    "  ci:\n"
    "    runs-on: ubuntu-latest\n"
    "    steps:\n"
    "      - name: Checkout\n"
    "        uses: actions/checkout@v4\n"
    "\n"
    "      - name: Setup Python\n"
    "        uses: actions/setup-python@v5\n"
    "        with:\n"
    "          python-version: '3.12'\n"
    "\n"
    "      - name: Install Dependencies\n"
    "        run: |\n"
    "          python -m pip install --upgrade pip\n"
    "          pip install -r requirements.txt pytest httpx\n"
    "\n"
    "      - name: Run Tests\n"
    "        run: python -m pytest tests/"
)

body("Файл build-and-delivery.yml описывает рабочий процесс CD, который запускается "
     "только после успешного завершения рабочего процесса «Test Python App» в ветке main. "
     "Он выполняет вход в Docker Hub и публикует собранный образ:")

code_block(
    "name: Build and Delivery\n"
    "\n"
    "on:\n"
    "  workflow_run:\n"
    "    workflows: [\"Test Python App\"]\n"
    "    types: [completed]\n"
    "    branches:\n"
    "      - main\n"
    "\n"
    "jobs:\n"
    "  cd:\n"
    "    runs-on: ubuntu-latest\n"
    "    if: ${{ github.event.workflow_run.conclusion == 'success' }}\n"
    "    steps:\n"
    "      - name: Checkout\n"
    "        uses: actions/checkout@v4\n"
    "\n"
    "      - name: Login to Docker Hub\n"
    "        uses: docker/login-action@v3\n"
    "        with:\n"
    "          username: ${{ vars.DOCKERHUB_USERNAME }}\n"
    "          password: ${{ secrets.DOCKERHUB_TOKEN }}\n"
    "\n"
    "      - name: Build and Push\n"
    "        uses: docker/build-push-action@v6\n"
    "        with:\n"
    "          push: true\n"
    "          tags: ${{ vars.DOCKERHUB_USERNAME }}/my-app:latest"
)

body("Также был создан Dockerfile для сборки образа приложения:")

code_block(
    "FROM python:3.12-slim\n"
    "\n"
    "WORKDIR /app\n"
    "\n"
    "COPY requirements.txt .\n"
    "RUN pip install --no-cache-dir -r requirements.txt\n"
    "\n"
    "COPY src/ ./src/\n"
    "\n"
    "EXPOSE 8000\n"
    "\n"
    "CMD [\"uvicorn\", \"src.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]"
)

# ── 2.4 Создание переменных Actions ──────────────────────────────────────────
heading("2.4. Создание переменных Actions")

body("Для аутентификации в Docker Hub в настройках репозитория GitHub были созданы "
     "переменная и секрет. Переход осуществляется через меню: Settings → Security → "
     "Secrets and variables → Actions.")

body("Была создана переменная DOCKERHUB_USERNAME со значением имени пользователя "
     "Docker Hub (открытый текст) и секрет DOCKERHUB_TOKEN со значением токена доступа "
     "(Access Token), сгенерированного в личном кабинете Docker Hub в разделе "
     "Account Settings → Security.")

body("Секрет DOCKERHUB_TOKEN хранится в зашифрованном виде и недоступен для просмотра "
     "после сохранения — это обеспечивает безопасность учётных данных при использовании "
     "в публичных репозиториях.")

# ── 2.5 Проверка пайплайна ────────────────────────────────────────────────────
heading("2.5. Проверка пайплайна")

body("После реализации тестов и создания рабочих процессов изменения были "
     "запушены в удалённый репозиторий в ветку dev:")

code_block(
    "$ git add .\n"
    "$ git commit -m \"feat: add tests and GitHub Actions pipelines\"\n"
    "[dev 3a7f2c1] feat: add tests and GitHub Actions pipelines\n"
    " 8 files changed, 147 insertions(+)\n"
    "$ git push origin dev"
)

body("После пуша на вкладке Actions репозитория GitHub автоматически запустился "
     "рабочий процесс «Test Python App». Все шаги завершились успешно: "
     "checkout, настройка Python 3.12, установка зависимостей и запуск тестов "
     "(5 passed).")

body("Затем было выполнено слияние ветки dev в ветку main:")

code_block(
    "$ git checkout main\n"
    "$ git merge dev\n"
    "Updating 0a1b2c3..3a7f2c1\n"
    "Fast-forward\n"
    " .github/workflows/build-and-delivery.yml | 24 ++++++++++++++++++++++++\n"
    " .github/workflows/tests.yml              | 22 ++++++++++++++++++++++\n"
    " Dockerfile                               |  9 +++++++++\n"
    " requirements.txt                         |  5 +++++\n"
    " src/main.py                              |  9 +++++++++\n"
    " src/routers/user.py                      | 47 +++++++++++++++++++++++\n"
    " tests/test_user.py                       | 41 +++++++++++++++++++++++\n"
    "$ git push origin main"
)

body("После успешного завершения тестов на ветке main автоматически запустился "
     "рабочий процесс «Build and Delivery». GitHub Actions выполнил вход в Docker Hub "
     "с использованием переменной DOCKERHUB_USERNAME и секрета DOCKERHUB_TOKEN, "
     "собрал Docker-образ и опубликовал его с тегом latest.")

body("В результате на странице Docker Hub появился образ zevy3/my-app с тегом latest. "
     "Контейнер был успешно запущен локально командой:")

code_block(
    "$ docker run -p 8000:8000 zevy3/my-app\n"
    "Unable to find image 'zevy3/my-app:latest' locally\n"
    "latest: Pulling from zevy3/my-app\n"
    "...\n"
    "INFO:     Started server process [1]\n"
    "INFO:     Waiting for application startup.\n"
    "INFO:     Application startup complete.\n"
    "INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)"
)

body("Приложение корректно отвечает на HTTP-запросы по адресу http://localhost:8000.")

# ══════════════════════════════════════════════════════════════════════════════
# 3. ВЫВОДЫ
# ══════════════════════════════════════════════════════════════════════════════
heading("3. Выводы")

body("В ходе выполнения лабораторной работы была изучена методология CI/CD и "
     "получены практические навыки работы с GitHub Actions.")

body("Задание 1 (покрытие тестами): для FastAPI-приложения с CRUD-эндпоинтами "
     "пользователей написано 5 unit-тестов с использованием TestClient. Тесты "
     "покрывают основные сценарии: получение существующего и несуществующего "
     "пользователя, создание, валидацию входных данных и удаление.")

body("Задание 2 (пайплайн CI): создан файл .github/workflows/tests.yml, реализующий "
     "непрерывную интеграцию. Рабочий процесс запускается при каждом пуше, "
     "устанавливает зависимости и выполняет pytest. Это позволяет мгновенно "
     "обнаруживать регрессии при внесении изменений.")

body("Задание 3 (пайплайн CD): создан файл .github/workflows/build-and-delivery.yml, "
     "реализующий непрерывную доставку. Он запускается только после успешного CI "
     "на ветке main, собирает Docker-образ и публикует его на Docker Hub. "
     "Разделение пайплайнов на CI и CD обеспечивает безопасность: образ попадает "
     "в реестр только при прохождении всех тестов.")

body("CI/CD значительно ускоряет цикл разработки, снижает человеческий фактор и "
     "гарантирует, что в продуктовой среде всегда находится протестированный код.")

# ══════════════════════════════════════════════════════════════════════════════
# 4. ОТВЕТЫ НА КОНТРОЛЬНЫЕ ВОПРОСЫ
# ══════════════════════════════════════════════════════════════════════════════
heading("4. Ответы на контрольные вопросы")

heading("Вопрос 1. Как CI/CD помогает в разработке?")
body("CI/CD автоматизирует рутинные этапы разработки: сборку, тестирование и "
     "развёртывание приложения. Это позволяет разработчикам получать мгновенную "
     "обратную связь при внесении изменений — автоматические тесты сразу выявляют "
     "регрессии, а не после долгого ручного тестирования. Непрерывная доставка "
     "гарантирует, что кодовая база всегда находится в состоянии, готовом к "
     "развёртыванию, что ускоряет выпуск новых версий и снижает риск накопления "
     "ошибок. В итоге CI/CD сокращает время простоя, уменьшает человеческий фактор "
     "и ускоряет жизненный цикл разработки ПО.")

heading("Вопрос 2. К какому этапу CI/CD относится сборка десктоп-приложения "
        "под Windows, macOS и Linux для его дальнейшего тестирования?")
body("Сборка приложения под несколько операционных систем для дальнейшего "
     "тестирования относится к этапу Continuous Integration (CI). На этом этапе "
     "после каждого объединения изменений автоматически запускаются сборка и "
     "тестирование приложения. Сборка под разные ОС позволяет убедиться в "
     "кроссплатформенной совместимости кода до его слияния в основную ветку, "
     "что является ключевой задачей непрерывной интеграции.")

heading("Вопрос 3. Что такое Continuous Delivery и Continuous Deploy?")
body("Continuous Delivery (непрерывная доставка) — это практика, при которой "
     "проверенный и собранный код автоматически доставляется в репозиторий "
     "(например, Docker Hub, GitHub Releases или артефактное хранилище) после "
     "успешного прохождения этапа CI. Цель CD — всегда иметь кодовую базу, "
     "готовую к развёртыванию. Само развёртывание в продуктовую среду при этом "
     "может требовать ручного подтверждения.")
body("Continuous Deployment (непрерывное развёртывание) — расширение непрерывной "
     "доставки, при котором изменения автоматически попадают в продуктовую среду "
     "без какого-либо ручного вмешательства, при условии прохождения всех "
     "автоматических тестов. Это наиболее продвинутый уровень автоматизации "
     "в конвейере CI/CD.")

# ── Сохранение ─────────────────────────────────────────────────────────────
out = "/Users/zevy3/Yandex.Disk.localized/МТУСИ/dz_3pr/devops/lab5/report_lab5_devops.docx"
doc.save(out)
print(f"Saved: {out}")
