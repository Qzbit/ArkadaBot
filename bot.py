# bot.py: Главный файл для запуска бота

import logging
import signal
import sys
from telebot import TeleBot
from handlers import start, admin, reminders, subscription, referral, star_pythagoras_handler
from database.models import init_db
from config import API_TOKEN


# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Инициализация бота
def initialize_bot():
    """Инициализирует экземпляр бота."""
    try:
        bot_instance = TeleBot(API_TOKEN)
        logger.info("Bot initialized successfully.")
        return bot_instance
    except Exception as e:
        logger.critical(f"Failed to initialize bot: {e}")
        sys.exit(1)

# Регистрация обработчиков
def register_handlers(bot_instance):
    """Регистрация всех обработчиков бота."""
    try:
        start.register_handlers(bot_instance)
        admin.register_handlers(bot_instance)
        reminders.register_handlers(bot_instance)
        subscription.register_handlers(bot_instance)
        referral.register_handlers(bot_instance)
        star_pythagoras_handler.register_handlers(bot_instance)  # Регистрация обработчика Звезды Пифагора
        logger.info("Handlers registered successfully.")
    except Exception as e:
        logger.error(f"Failed to register handlers: {e}")
        sys.exit(1)

# Обработка сигнала завершения работы
def handle_exit_signal(signal_received, frame):
    """Обрабатывает сигналы завершения работы."""
    logger.info("Received termination signal. Bot is shutting down...")
    sys.exit(0)

# Запуск бота
if __name__ == "__main__":
    try:
        # Инициализация базы данных
        init_db()
        logger.info("Database initialized successfully.")

        # Инициализация бота
        bot = initialize_bot()

        # Регистрация обработчиков
        register_handlers(bot)

        # Обработка сигналов завершения
        signal.signal(signal.SIGINT, handle_exit_signal)
        signal.signal(signal.SIGTERM, handle_exit_signal)

        # Запуск бота
        logger.info("Bot is running...")
        bot.infinity_polling()

    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.error(f"An unhandled error occurred: {e}")
        sys.exit(1)
