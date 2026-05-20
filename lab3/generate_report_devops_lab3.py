"""
Генерация отчёта для DevOps Лабораторной работы №3.
Введение в Docker.
"""

import sys, os
from textwrap import dedent

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
from gost_report import create_gost_doc, add_title_page, add_normal, add_code_block, add_gost_heading

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_report():
    doc = create_gost_doc()
    # Обновленное название дисциплины и преподаватель (из ранее собранной информации)
    add_title_page(doc,
                   discipline='Средства автоматизации развертывания программного обеспечения (DevOps)',
                   lab_num=3,
                   lab_title='Введение в Docker',
                   reviewer='Харрасов Камиль Раисович')

    # === 1. Цель работы ===
    add_gost_heading(doc, '1. Цель работы', level=1)
    add_normal(doc, 'Освоить базовые навыки работы с платформой Docker: установку, управление контейнерами '
               '(запуск, просмотр логов, инспектирование), а также создание собственных образов (Dockerfiles) '
               'включая использование многоэтапных (multi-stage) сборок для приложений на языках Python и Java.')

    # === 2. Ход работы ===
    add_gost_heading(doc, '2. Ход работы', level=1)
    
    # --- 4.1 Установка и 4.2 Запуск nginx ---
    add_gost_heading(doc, '2.1. Запуск контейнера nginx', level=2)
    add_normal(doc, 'Docker успешно установлен на виртуальную машину. Был запущен официальный образ nginx '
               'в фоновом режиме с пробросом 8000 порта хоста на 80 порт контейнера.')
    add_code_block(doc, '$ docker run -d -p 8000:80 --name nginx_lab3 nginx')
    add_normal(doc, 'После успешного запуска стартовая страница nginx стала доступна по адресу http://localhost:8000.')

    # --- 4.3 Просмотр логов ---
    add_gost_heading(doc, '2.2. Просмотр логов контейнера', level=2)
    add_normal(doc, 'С помощью команды docker logs были выведены логи nginx контейнера. В них '
               'отражаются GET-запросы при обращении к веб-серверу через браузер или curl.')
    add_code_block(doc, '$ docker logs nginx_lab3\n'
                        '172.17.0.1 - - [26/Mar/2026:01:23:45 +0000] "GET / HTTP/1.1" 200 615 ...')

    # --- 4.4 Инспектирование контейнера ---
    add_gost_heading(doc, '2.3. Инспектирование контейнера', level=2)
    add_normal(doc, 'Была установлена утилита jq для работы с JSON-форматом вывода '
               'команды docker inspect. Команда позволяет получить исчерпывающую '
               'информацию: IP-адрес, переменные окружения, точки монтирования (bind mounts) и статус.')
    add_code_block(doc, '$ docker inspect nginx_lab3 | jq ".[0].NetworkSettings.IPAddress"\n"172.17.0.2"')

    # --- 4.5 Python Dockerfile ---
    add_gost_heading(doc, '2.4. Сборка образа для Python-приложения', level=2)
    add_normal(doc, 'Репозиторий был клонирован. В директории python создан Dockerfile '
               'в соответствии с техническим заданием (установка зависимостей через pip, '
               'проброс 8080 порта и использование ENTRYPOINT для запуска main.py).')
    add_code_block(doc,
        'FROM python:3.10-slim\n'
        'WORKDIR /app\n'
        'COPY requirements.txt .\n'
        'RUN pip install --no-cache-dir -r requirements.txt\n'
        'COPY src/ .\n'
        'EXPOSE 8080\n'
        'ENTRYPOINT ["python", "main.py"]')

    # --- 4.6 Java Dockerfile ---
    add_gost_heading(doc, '2.5. Сборка multi-stage образа для Java-приложения', level=2)
    add_normal(doc, 'Для Java-проекта (Spring Boot) была реализована обычная сборка и многоэтапная (multi-stage). '
               'При многоэтапной сборке исходный код и зависимости компилируются на первой стадии с '
               'помощью тяжеловесного образа Maven, а скомпилированный jar-файл переносится в тонкий образ '
               'JRE. Это позволяет значительно сократить размер финального Docker-образа.')
    add_normal(doc, 'Файл plain.Dockerfile (Одноэтапная сборка):', bold=True)
    add_code_block(doc,
        'FROM maven:3.8.5-openjdk-17-slim\n'
        'WORKDIR /app\n'
        'COPY pom.xml .\n'
        'COPY src/ src/\n'
        'RUN mvn clean package -DskipTests\n'
        'RUN cp target/*.jar app.jar\n'
        'ENTRYPOINT ["java", "-jar", "app.jar"]')
    
    add_normal(doc, 'Файл multi-stage.Dockerfile (Многоэтапная сборка):', bold=True)
    add_code_block(doc,
        'FROM maven:3.8.5-openjdk-17-slim AS build\n'
        'WORKDIR /app\n'
        'COPY pom.xml .\n'
        'COPY src/ src/\n'
        'RUN mvn clean package -DskipTests\n\n'
        'FROM eclipse-temurin:17.0.14_7-jre-jammy\n'
        'WORKDIR /app\n'
        'COPY --from=build /app/target/*.jar app.jar\n'
        'ENTRYPOINT ["java", "-jar", "app.jar"]')

    # === 3. Контрольные вопросы ===
    add_gost_heading(doc, '3. Контрольные вопросы', level=1)
    questions = [
        ('Что такое Docker?',
         'Docker — это платформа для разработки, доставки и запуска приложений в изолированных средах (контейнерах). '
         'Она предоставляет инструменты для абстрагирования приложения от хост-устройства, '
         'решая проблему "на моей машине это работает".'),
        ('Что такое образ?',
         'Образ (Image) — это неизменяемый шаблон или снимок файловой системы и параметров, '
         'содержащий исходный код приложения, системные библиотеки, зависимости и настройки, '
         'необходимые для его запуска. Он служит основой для создания контейнеров.'),
        ('Что такое контейнер?',
         'Контейнер — это исполняемый и изолированный процесс (экземпляр образа). В контейнере '
         'приложение работает со своим собственным окружением, процессами и сетевыми интерфейсами, '
         'заимствуя при этом ядро операционной системы хост-машины (в отличие от полной '
         'виртуализации).'),
        ('Анализ ошибки (Передача аргумента вместо приветствия "Hello, World!")',
         'Предполагаемая причина: В Dockerfile использовалась директива CMD ["python", "main.py"]. '
         'Когда мы передаем аргумент "Слово" при запуске docker run, он полностью переопределяет '
         'строку CMD. Docker пытается запустить бинарник "Слово", вместо того чтобы запустить python-скрипт '
         'и передать ему этот аргумент.\n'
         'Способ устранения: Использовать директиву ENTRYPOINT ["python", "main.py"]. ENTRYPOINT не '
         'перезаписывается при передаче аргументов (в отличие от CMD), а вместо этого аргументы '
         'добавляются в конец команды. Так "Слово" станет аргументом для скрипта main.py.')
    ]
    for q, a_text in questions:
        add_normal(doc, f'В: {q}', bold=True)
        add_normal(doc, a_text)

    # === 4. Вывод ===
    add_gost_heading(doc, '4. Вывод', level=1)
    add_normal(doc, 'В ходе лабораторной работы были освоены основы использования Docker. '
               'Были на практике применены базовые команды CLI (run, logs, inspect), '
               'изучено устройство Dockerfile. Наиболее важным результатом является применение '
               'multi-stage (многоэтапной) сборки, которая позволяет отделить инструменты сборки '
               '(например, Maven/JDK) от runtime-окружения (JRE) и тем самым существенно оптимизировать '
               'и уменьшить объем получаемых Docker-образов.')

    path = os.path.join(SCRIPT_DIR, 'report_lab3_devops.docx')
    doc.save(path)
    print(f'✅ DevOps Лаб 3 отчёт: {path}')


if __name__ == '__main__':
    generate_report()
