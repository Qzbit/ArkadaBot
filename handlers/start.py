from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from templates.messages import WELCOME_MESSAGE
from handlers.star_pythagoras_handler import handle_star_pythagoras
import logging
from calculators.calculator_utils import get_description

# Настройка логирования
logger = logging.getLogger(__name__)

def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        """Отображает главное меню с вертикальными кнопками."""
        try:
            # Главное меню
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(InlineKeyboardButton("Калькуляторы", callback_data="calculators"))
            keyboard.add(InlineKeyboardButton("Подписка", callback_data="subscription"))
            keyboard.add(InlineKeyboardButton("Реферальная система", callback_data="referral"))
            keyboard.add(InlineKeyboardButton("Матрица знаний", callback_data="knowledge"))

            bot.send_message(
                message.chat.id,
                WELCOME_MESSAGE.format(user=message.chat.first_name or "Пользователь"),
                reply_markup=keyboard
            )
        except Exception as e:
            logger.error(f"Ошибка в 'send_welcome': {e}")
            bot.send_message(message.chat.id, "Произошла ошибка. Попробуйте позже.")

    @bot.callback_query_handler(func=lambda call: call.data == "calculators")
    def show_calculators(call):
        """Показывает подменю с калькуляторами."""
        try:
            keyboard = InlineKeyboardMarkup(row_width=1)
            keyboard.add(InlineKeyboardButton("Звезда Пифагора", callback_data="pythagoras"))
            keyboard.add(InlineKeyboardButton("Число личного дня", callback_data="personal_day"))
            keyboard.add(InlineKeyboardButton("Число арканы", callback_data="arcanum"))
            keyboard.add(InlineKeyboardButton("Число богатства", callback_data="wealth"))
            keyboard.add(InlineKeyboardButton("Назад", callback_data="main_menu"))

            bot.edit_message_text(
                "Выберите калькулятор:",
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=keyboard
            )
        except Exception as e:
            logger.error(f"Ошибка в 'show_calculators': {e}")
            bot.send_message(call.message.chat.id, "Произошла ошибка. Попробуйте позже.")

    @bot.callback_query_handler(func=lambda call: call.data == "pythagoras")
    def handle_pythagoras(call):
        """Обрабатывает выбор 'Звезда Пифагора'."""
        try:
            bot.send_message(call.message.chat.id, "Введите вашу дату рождения в формате ДД.ММ.ГГГГ:")
            bot.register_next_step_handler(call.message, process_pythagoras)
        except Exception as e:
            logger.error(f"Ошибка в 'handle_pythagoras': {e}")
            bot.send_message(call.message.chat.id, "Произошла ошибка. Попробуйте позже.")

    def process_pythagoras(message):
        """Обрабатывает ввод для Звезды Пифагора и генерирует изображение."""
        try:
            birth_date = message.text.strip()
            # Передача даты в обработчик
            image_path = handle_star_pythagoras(birth_date)
            
            if image_path:
                with open(image_path, 'rb') as image:
                    bot.send_photo(
                        message.chat.id,
                        photo=image,
                        caption="Ваша Звезда Пифагора успешно рассчитана!"
                    )
            else:
                bot.send_message(message.chat.id, "Не удалось сгенерировать изображение. Попробуйте позже.")
        except ValueError:
            bot.send_message(message.chat.id, "Ошибка! Убедитесь, что дата введена в формате ДД.ММ.ГГГГ.")
        except Exception as e:
            logger.error(f"Ошибка генерации изображения: {e}")
            bot.send_message(message.chat.id, "Произошла ошибка при генерации. Попробуйте позже.")

    @bot.callback_query_handler(func=lambda call: call.data == "personal_day")
    def handle_personal_day(call):
        """Обрабатывает расчет числа личного дня."""
        bot.send_message(call.message.chat.id, "Введите вашу дату рождения в формате ДД.ММ.ГГГГ:")
        bot.register_next_step_handler(call.message, process_personal_day)

    def process_personal_day(message):
        """Обрабатывает дату для расчета числа личного дня."""
        try:
            birth_date = message.text.strip()
            day, month, year = map(int, birth_date.split('.'))
            result = calculate_personal_day(day, month, year)
            description = get_description("personal_day", result)
            bot.send_message(message.chat.id, f"Ваше Число личного дня: {result}\n\n{description}")
        except ValueError:
            bot.send_message(message.chat.id, "Ошибка! Убедитесь, что дата введена в формате ДД.ММ.ГГГГ.")
        except Exception as e:
            logger.error(f"Ошибка при расчете числа личного дня: {e}")
            bot.send_message(message.chat.id, "Произошла ошибка. Попробуйте позже.")
