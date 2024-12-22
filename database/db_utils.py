import sqlite3
import logging
from database.models import DB_PATH

# Настройка логирования
logger = logging.getLogger(__name__)

# Получить соединение с базой данных
def get_connection():
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        logger.critical(f"Ошибка при подключении к базе данных: {e}")
        raise SystemExit("Не удалось подключиться к базе данных.")

# Универсальная функция для выполнения SQL-запросов
def execute_query(query, params=(), fetchone=False, fetchall=False):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = None
        return result
    except sqlite3.Error as e:
        logger.error(f"Ошибка при выполнении SQL-запроса: {e}\nЗапрос: {query}")
        return None
    finally:
        conn.close()

# Обновить дату окончания подписки
def update_subscription(user_id, new_expiry_date):
    """Обновляет дату окончания подписки для указанного пользователя."""
    query = """
        UPDATE users
        SET subscription_end = ?
        WHERE id = ?
    """
    execute_query(query, (new_expiry_date.strftime("%Y-%m-%d"), user_id))
    logger.info(f"Subscription updated for user {user_id} to {new_expiry_date}")

# Получить всех пользователей
def get_all_users():
    """Возвращает список всех пользователей с их статусом и временем напоминания."""
    query = """
        SELECT id, status, subscription_end, reminder_time
        FROM users
    """
    users = execute_query(query, fetchall=True)
    if users:
        logger.info("Fetched all users from database")
    return [{"id": row[0], "status": row[1], "subscription_end": row[2], "reminder_time": row[3]} for row in users]

# Обновить описание текста
def update_text_description(identifier, new_text):
    """Обновляет описание текста в базе данных по идентификатору."""
    query = """
        UPDATE descriptions
        SET text = ?
        WHERE identifier = ?
    """
    execute_query(query, (new_text, identifier))
    logger.info(f"Text description updated for {identifier}")

# Добавить нового пользователя
def add_user(user_id, status, subscription_end):
    """Добавляет нового пользователя в базу данных."""
    query_check = "SELECT 1 FROM users WHERE id = ?"
    if execute_query(query_check, (user_id,), fetchone=True):
        logger.warning(f"Пользователь {user_id} уже существует.")
        raise ValueError("Пользователь уже существует.")
    query_add = """
        INSERT INTO users (id, status, subscription_end)
        VALUES (?, ?, ?)
    """
    execute_query(query_add, (user_id, status, subscription_end))
    logger.info(f"User {user_id} added successfully")

# Сохранить время напоминания
def save_reminder_time(user_id, reminder_time):
    """Сохраняет время напоминания для пользователя."""
    query = """
        UPDATE users
        SET reminder_time = ?
        WHERE id = ?
    """
    execute_query(query, (reminder_time, user_id))
    logger.info(f"Reminder time {reminder_time} saved for user {user_id}")

# Получить время напоминания
def get_reminder_time(user_id):
    """Возвращает время напоминания для указанного пользователя."""
    query = """
        SELECT reminder_time
        FROM users
        WHERE id = ?
    """
    result = execute_query(query, (user_id,), fetchone=True)
    if result:
        logger.info(f"Fetched reminder time for user {user_id}: {result[0]}")
    return result[0] if result else None

# Добавить реферала
def add_referral(new_user_id, referrer_id):
    """Добавляет реферала и связывает его с реферером."""
    query_check = "SELECT 1 FROM referrals WHERE referred_id = ?"
    if execute_query(query_check, (new_user_id,), fetchone=True):
        logger.warning(f"Пользователь {new_user_id} уже зарегистрирован через реферальную ссылку.")
        raise ValueError("Пользователь уже зарегистрирован через реферальную ссылку.")
    query_add = """
        INSERT INTO referrals (referrer_id, referred_id)
        VALUES (?, ?)
    """
    execute_query(query_add, (referrer_id, new_user_id))
    logger.info(f"Referral added: referrer {referrer_id}, referred {new_user_id}")

# Получить ID реферера
def get_referer_id(user_id):
    """Возвращает ID реферера для указанного пользователя."""
    query = """
        SELECT referrer_id
        FROM referrals
        WHERE referred_id = ?
    """
    try:
        result = execute_query(query, (user_id,), fetchone=True)
        return result[0] if result else None
    except Exception as e:
        logger.error(f"Ошибка при получении ID реферера для пользователя {user_id}: {e}")
        return None
