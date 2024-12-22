import json
import os

def get_description(calculator, result):
    """Возвращает описание для результата из JSON."""
    try:
        file_path = os.path.join("templates", "descriptions", f"{calculator}.json")
        with open(file_path, "r", encoding="utf-8") as file:
            descriptions = json.load(file)
        return descriptions.get(str(result), "Описание не найдено.")
    except Exception as e:
        return f"Ошибка при загрузке описания: {e}"
