import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes


TOKEN = " ТОКЕН ВАМ НЕ ДАМ))) "


# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎲 Начать игру", callback_data='start_game')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я бот для игры в 'Камень, ножницы, бумага'.\n"
        "Нажми кнопку ниже, чтобы начать игру!",
        reply_markup=reply_markup
    )


# Обработка команды /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Правила игры:\n"
        "- Камень побеждает ножницы\n"
        "- Ножницы побеждают бумагу\n"
        "- Бумага побеждает камень\n\n"
        "Используйте команду /start для начала игры!"
    )


# Запуск игры
async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("🗿 Камень", callback_data='rock'),
            InlineKeyboardButton("✂️ Ножницы", callback_data='scissors'),
        ],
        [
            InlineKeyboardButton("📄 Бумага", callback_data='paper'),
            InlineKeyboardButton("❌ Отмена", callback_data='cancel')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "Выберите ваш ход:",
        reply_markup=reply_markup
    )


# Обработка хода игрока
async def player_move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_choice = query.data
    bot_choice = random.choice(['rock', 'scissors', 'paper'])

    # Определение победителя
    result = determine_winner(user_choice, bot_choice)

    # Эмодзи для отображения выбора
    choices_emoji = {
        'rock': '🗿 Камень',
        'paper': '📄 Бумага',
        'scissors': '✂️ Ножницы'
    }

    # Формирование ответа
    response = (
        f"Ваш выбор: {choices_emoji[user_choice]}\n"
        f"Мой выбор: {choices_emoji[bot_choice]}\n\n"
        f"Результат: {result}"
    )

    # Добавляем кнопки для новой игры
    keyboard = [
        [
            InlineKeyboardButton("🔄 Начать сначала", callback_data='start_game'),
            InlineKeyboardButton("🏁 Завершить", callback_data='finish')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(response, reply_markup=reply_markup)


# Завершение игры
async def finish_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "Игра завершена!\n"
        "Чтобы сыграть снова, используйте /start"
    )


# Отмена игры
async def cancel_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Игра отменена. Используйте /start для новой игры.")


# Логика определения победителя
def determine_winner(user: str, bot: str) -> str:
    if user == bot:
        return "Ничья! 😐"

    win_conditions = {
        'rock': 'scissors',  # Камень побеждает ножницы
        'scissors': 'paper',  # Ножницы побеждают бумагу
        'paper': 'rock'  # Бумага побеждает камень
    }

    if win_conditions[user] == bot:
        return "Вы победили! 🎉"
    else:
        return "Я победил! 🤖"


# Настройка и запуск бота
def main():
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Регистрация обработчиков кнопок
    application.add_handler(CallbackQueryHandler(start_game, pattern='start_game'))
    application.add_handler(CallbackQueryHandler(cancel_game, pattern='cancel'))
    application.add_handler(CallbackQueryHandler(finish_game, pattern='finish'))
    application.add_handler(CallbackQueryHandler(player_move, pattern='^(rock|paper|scissors)$'))

    # Запуск бота
    print("Бот запущен...")
    application.run_polling()


if __name__ == '__main__':
    main()
