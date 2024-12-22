from PIL import Image, ImageDraw, ImageFont
import os

# Логика расчёта чисел звезды
def calculate_star_pythagoras(day, month, year):
    """Выполняет расчёты для Звезды Пифагора."""
    def reduce_to_single_digit(num):
        while num > 9:
            num = sum(int(d) for d in str(num))
        return num

    day_number = reduce_to_single_digit(day)
    month_number = reduce_to_single_digit(month)
    year_number = reduce_to_single_digit(sum(int(d) for d in str(year)))
    sum1 = reduce_to_single_digit(day_number + month_number + year_number)
    sum2 = reduce_to_single_digit(day_number + month_number + year_number + sum1)
    center = reduce_to_single_digit(day_number + month_number + year_number + sum1 + sum2)

    return {
        "day": day_number,
        "month": month_number,
        "year": year_number,
        "sum1": sum1,
        "sum2": sum2,
        "center": center,
    }

# Генерация изображения
def generate_star_image(results):
    """Генерирует изображение Звезды Пифагора с рассчитанными значениями."""
    try:
        # Пути к файлам
        template_path = os.path.join("templates", "star_pythagoras_template.png")
        output_path = os.path.join("generated_images", "star_pythagoras_result.png")
        font_path = os.path.join("fonts", "arial.ttf")

        # Проверка наличия файлов
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Шаблон не найден: {template_path}")
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Шрифт не найден: {font_path}")

        # Убедиться, что директория для результата существует
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Открытие шаблона
        image = Image.open(template_path).convert("RGBA")
        draw = ImageDraw.Draw(image)

        # Загрузка шрифта
        try:
            font_bold = ImageFont.truetype(font_path, 40)  # Жирный шрифт для центра
            font = ImageFont.truetype(font_path, 32)      # Обычный шрифт для остальных чисел
        except IOError:
            raise FileNotFoundError(f"Ошибка загрузки шрифта: {font_path}")

        # Координаты для текста
        positions = {
            "day": (20, 140),     # Верхняя точка
            "month": (230, 45),   # Правая верхняя точка
            "year": (385, 140),   # Правая нижняя точка
            "sum1": (340, 385),   # Левая нижняя точка
            "sum2": (60, 380),    # Левая верхняя точка
            "center": (205, 200)  # Центр
        }

        # Добавление текста на изображение
        for key, position in positions.items():
            if key == "center":
                draw.text(position, str(results[key]), font=font_bold, fill="white", anchor="mm")
            else:
                draw.text(position, str(results[key]), font=font, fill="white", anchor="mm")

        # Сохранение результата
        image.save(output_path)
        return output_path

    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")
        return None
    except Exception as e:
        print(f"Ошибка при генерации изображения: {e}")
        return None
