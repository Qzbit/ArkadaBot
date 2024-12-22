# handlers/subscription.py: Обработчик подписки

from datetime import datetime, timedelta
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from database.db_utils import update_subscription

def register_handlers(bot):

    @bot.message_handler(commands=['subscription'])
    def manage_subscription(message):
        user_id = message.chat.id

        # Проверяем статус пользователя
        user_status = get_user_status(user_id)
        if user_status == "active":
            bot.send_message(user_id, "Ваша подписка активна.")
        else:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(KeyboardButton("Продлить подписку"))
            bot.send_message(user_id, "Ваша подписка истекла. Продлите её для доступа ко всем функциям.", reply_markup=keyboard)

    @bot.message_handler(func=lambda message: message.text == "Продлить подписку")
    def extend_subscription(message):
        user_id = message.chat.id

        # Продлеваем подписку на 30 дней (можно подключить платежную систему)
        new_expiry_date = datetime.now() + timedelta(days=30)
        update_subscription(user_id, new_expiry_date)

        bot.send_message(user_id, f"Подписка успешно продлена до {new_expiry_date.strftime('%Y-%m-%d')}.")

# Заглушка для статуса пользователя
def get_user_status(user_id):
    # Заглушка: использовать функцию из базы данных
    return "inactive"
