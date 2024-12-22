from datetime import datetime
from telebot import TeleBot
from database.db_utils import get_all_users, save_reminder_time, get_reminder_time
from handlers.utils import is_subscription_active

def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['set_reminder'])
    def set_reminder(message):
        bot.send_message(
            message.chat.id,
            "Пожалуйста, выберите время для ежедневного напоминания (например, 09:00):"
        )
        bot.register_next_step_handler(message, save_reminder_time_handler)

    def save_reminder_time_handler(message):
        user_id = message.chat.id
        reminder_time = message.text

        try:
            datetime.strptime(reminder_time, "%H:%M")
            save_reminder_time(user_id, reminder_time)  # Сохраняем в базу
            bot.send_message(
                user_id,
                f"Напоминание успешно установлено на {reminder_time}."
            )
        except ValueError:
            bot.send_message(
                user_id,
                "Неверный формат времени. Пожалуйста, используйте формат ЧЧ:ММ (например, 09:00)."
            )

def send_daily_reminders(bot: TeleBot):
    users = get_all_users()
    current_time = datetime.now().strftime("%H:%M")

    for user in users:
        user_id = user["id"]
        reminder_time = get_reminder_time(user_id)  # Получаем время напоминания из базы

        if reminder_time == current_time and is_subscription_active(user["subscription_end"]):
            bot.send_message(
                user_id,
                "Ваше ежедневное напоминание: Сегодняшний день принесет новые возможности!"
            )
