# handlers/referral.py: Логика реферальной системы

from database.db_utils import get_all_users

def register_handlers(bot):

    @bot.message_handler(commands=['referral'])
    def referral_system(message):
        user_id = message.chat.id
        referral_link = f"https://t.me/num_calc_bot?start=ref_{user_id}"
        
        bot.send_message(
            user_id,
            f"Ваша реферальная ссылка:\n{referral_link}\n\n"
            "Поделитесь этой ссылкой с друзьями. "
            "Вы получите бонус +1 месяц подписки, если ваш друг активирует подписку!"
        )
