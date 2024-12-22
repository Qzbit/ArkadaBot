# handlers/utils.py: Вспомогательные функции

from datetime import datetime, timedelta
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

# Форматирование даты в строку для отображения
# Например: 2024-12-31 -> "31 декабря 2024"
def format_date(date_obj):
    """Форматирует объект даты в строку 'день месяц год'."""
    try:
        return date_obj.strftime("%d %B %Y")
    except AttributeError as e:
        logger.error(f"Ошибка форматирования даты: {e}")
        return "Неизвестная дата"

# Проверка, активна ли подписка пользователя
def is_subscription_active(subscription_end):
    """Проверяет, активна ли подписка пользователя.

    Args:
        subscription_end (str): Дата окончания подписки в формате 'ГГГГ-ММ-ДД'.

    Returns:
        bool: True, если подписка активна, иначе False.
    """
    if not subscription_end:
        return False
    try:
        current_date = datetime.now()
        end_date = datetime.strptime(subscription_end, "%Y-%m-%d")
        return current_date <= end_date
    except ValueError as e:
        logger.error(f"Ошибка при проверке подписки: {e}")
        return False

# Рассчитать количество оставшихся дней подписки
def remaining_days(subscription_end):
    """Рассчитывает количество оставшихся дней подписки.

    Args:
        subscription_end (str): Дата окончания подписки в формате 'ГГГГ-ММ-ДД'.

    Returns:
        int: Количество дней до окончания подписки, 0 если подписка истекла.
    """
    if not subscription_end:
        return 0
    try:
        current_date = datetime.now()
        end_date = datetime.strptime(subscription_end, "%Y-%m-%d")
        delta = end_date - current_date
        return max(delta.days, 0)
    except ValueError as e:
        logger.error(f"Ошибка при расчете оставшихся дней подписки: {e}")
        return 0
