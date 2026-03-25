"""Консольное TODO-приложение с сохранением в JSON — улучшенная версия"""

import json
from pathlib import Path
import os
from datetime import datetime


TODO_FILE = Path("todo.json")


def clear_screen():
    """Очищает экран консоли."""
    os.system('cls' if os.name == 'nt' else 'clear')


def load_tasks() -> list[dict]:
    """Загружает задачи из JSON-файла."""
    if not TODO_FILE.exists():
        return []

    try:
        with TODO_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("⚠️ Файл todo.json повреждён. Начинаем с пустого списка.")
        return []


def save_tasks(tasks: list[dict]) -> None:
    """Сохраняет задачи в JSON-файл."""
    try:
        with TODO_FILE.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=2)
    except OSError:
        print("⚠️ Не удалось сохранить файл todo.json")


def show_tasks(tasks: list[dict]) -> None:
    """Показывает все задачи."""
    clear_screen()
    print("\n" + "=" * 50)
    print("📋 МОЙ СПИСОК ЗАДАЧ")
    print("=" * 50)

    if not tasks:
        print("🎉 Пока задач нет. Добавьте первую!")
        return

    for i, task in enumerate(tasks, 1):
        status = "✅" if task.get("done", False) else "⬜"
        text = task.get("text", "")
        created = task.get("created", "—")
        print(f"{i:2d}. {status} {text}   (создана: {created})")


def add_task(tasks: list[dict]) -> None:
    """Добавляет новую задачу."""
    text = input("\nВведите текст задачи: ").strip()
    if not text:
        print("⚠️ Задача не может быть пустой!")
        return

    tasks.append({
        "text": text,
        "done": False,
        "created": datetime.now().strftime("%d.%m.%Y %H:%M")
    })
    print("✅ Задача успешно добавлена!")


def get_task_index(tasks: list[dict], message: str) -> int | None:
    """Безопасно получает номер задачи."""
    if not tasks:
        print("⚠️ Список задач пуст.")
        return None

    try:
        num = int(input(message).strip())
        if 1 <= num <= len(tasks):
            return num - 1
        print("⚠️ Неверный номер задачи.")
        return None
    except ValueError:
        print("⚠️ Введите число!")
        return None


def delete_task(tasks: list[dict]) -> None:
    show_tasks(tasks)
    index = get_task_index(tasks, "\nВведите номер задачи для удаления: ")
    if index is None:
        return
    deleted_text = tasks.pop(index)["text"]
    print(f"🗑️ Задача удалена: {deleted_text}")


def mark_task_done(tasks: list[dict]) -> None:
    show_tasks(tasks)
    index = get_task_index(tasks, "\nВведите номер выполненной задачи: ")
    if index is None:
        return
    tasks[index]["done"] = True
    print(f"✅ Задача отмечена как выполненная: {tasks[index]['text']}")


def print_menu() -> None:
    print("\n" + "-" * 50)
    print("Выберите действие:")
    print("1 — Показать все задачи")
    print("2 — Добавить новую задачу")
    print("3 — Удалить задачу")
    print("4 — Отметить задачу как выполненную")
    print("5 — Выход и сохранение")
    print("-" * 50)


def main() -> None:
    tasks = load_tasks()
    print("🚀 Добро пожаловать в улучшенное TODO-приложение!")

    while True:
        print_menu()
        choice = input("\nВаш выбор: ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            delete_task(tasks)
        elif choice == "4":
            mark_task_done(tasks)
        elif choice == "5":
            save_tasks(tasks)
            print("💾 Задачи сохранены в todo.json")
            print("До свидания! 👋")
            break
        else:
            print("⚠️ Неверный выбор. Введите число от 1 до 5.")

        input("\nНажмите Enter, чтобы продолжить...")


if __name__ == "__main__":
    main()
