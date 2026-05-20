#!/bin/bash

usage() {
    echo "Использование:"
    echo "  $0 \"имя_файла\" \"/путь/к/директории\""
    echo "  $0 -p \"паттерн\" \"/путь/к/директории\""
    echo ""
    echo "Режимы:"
    echo "  Без флагов  — удаление файлов с точным именем."
    echo "  -p          — удаление файлов, содержащих паттерн в имени (подстрока, case-sensitive)."
    echo ""
    echo "Примеры:"
    echo "  $0 \"file.txt\" \"/home/user/docs\""
    echo "  $0 -p \"log\" \"/var/logs\""
    exit 1
}

PATTERN_MODE=false

if [[ "$1" == "-p" ]]; then
    PATTERN_MODE=true
    shift
fi

if [[ $# -ne 2 ]]; then
    echo "Ошибка: неверное количество аргументов."
    usage
fi

SEARCH_TERM="$1"
TARGET_DIR="$2"

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Ошибка: директория '$TARGET_DIR' не найдена."
    exit 1
fi

if [[ -z "$SEARCH_TERM" ]]; then
    echo "Ошибка: имя файла или паттерн не может быть пустым."
    usage
fi

DELETED_COUNT=0

cd "$TARGET_DIR" || {
    echo "Ошибка: не удалось перейти в директорию '$TARGET_DIR'."
    exit 1
}

if [[ "$PATTERN_MODE" == true ]]; then
    echo "Поиск файлов, содержащих '$SEARCH_TERM' в имени, в директории '$TARGET_DIR'..."
    while IFS= read -r -d '' file; do
        rel_path="${file#./}"
        echo "  Удаление: $rel_path"
        rm -- "$rel_path"
        ((DELETED_COUNT++))
    done < <(find . -type f -print0 | while IFS= read -r -d '' f; do
        filename=$(basename "$f")
        if [[ "$filename" == *"$SEARCH_TERM"* ]]; then
            printf '%s\0' "$f"
        fi
    done)
else
    echo "Поиск файлов с именем '$SEARCH_TERM' в директории '$TARGET_DIR'..."
    while IFS= read -r -d '' file; do
        rel_path="${file#./}"
        echo "  Удаление: $rel_path"
        rm -- "$rel_path"
        ((DELETED_COUNT++))
    done < <(find . -type f -name "$SEARCH_TERM" -print0)
fi

if [[ $DELETED_COUNT -eq 0 ]]; then
    echo "Файлы не найдены."
else
    echo "Удалено файлов: $DELETED_COUNT"
fi

exit 0
