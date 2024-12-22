# templates/messages.py: Шаблоны сообщений

WELCOME_MESSAGE = (
    "Добро пожаловать в Матрицу чисел! 🌌\n"
    "Откройте для себя значение чисел и их влияние на вашу жизнь. Наш бот поможет вам рассчитать:\n"
    "🔢 Число жизненного пути\n"
    "🃏 Арканы по дате рождения\n"
    "⭐ Звезду Пифагора и многое другое.\n\n"
    "Доступные функции:\n"
    "1️⃣ Калькуляторы — доступ к инструментам расчёта\n"
    "💎 Подписка — откройте доступ ко всем возможностям\n"
    "👥 Реферальная система — получайте бонусы за приглашения\n"
    "⏰ Напоминания — настройте ежедневные уведомления\n\n"
    "Начните прямо сейчас! Выберите интересующий вас раздел из меню ниже. 🚀"
)


ADMIN_WELCOME_MESSAGE = (
    "Добро пожаловать в панель администратора. Выберите действие:\n"
    "📋 Просмотр пользователей\n"
    "✏️ Изменить текст описания\n"
)

# Шаблоны для калькулятора "Число личного дня"
PERSONAL_DAY_MESSAGES = {
    "prompt": "Введите дату рождения в формате: ДД.ММ.ГГГГ",
    "error": "Ошибка! Убедитесь, что дата введена в формате: ДД.ММ.ГГГГ",
    "result": "Ваше число личного дня: {number}\n\n{description}"
}

ARCANUM_MESSAGES = {
    "prompt": "Введите дату рождения в формате: ДД.ММ.ГГГГ",
    "result": "Ваш аркан: {number}\n\n{description}",
    "error": "Ошибка! Убедитесь, что дата введена в формате: ДД.ММ.ГГГГ"
}