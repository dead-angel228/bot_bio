from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import logging

# Включаем логирование для отслеживания ошибок
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Этапы разговора
FEEDBACK, SUGGESTION = range(2)

# Команда /start
def start(update: Update, context):
    update.message.reply_text(
        "Привет! Я бот для обратной связи. Чем могу помочь?\n"
        "1. Оставить отзыв\n"
        "2. Предложить улучшение\n"
        "Выбери вариант:",
        reply_markup=ReplyKeyboardMarkup([['1', '2']], one_time_keyboard=True)
    )
    return FEEDBACK

# Обработка выбора пользователя
def feedback(update: Update, context):
    user_choice = update.message.text
    if user_choice == '1':
        update.message.reply_text("Напиши свой отзыв:")
        return SUGGESTION
    elif user_choice == '2':
        update.message.reply_text("Напиши свое предложение по улучшению:")
        return SUGGESTION
    else:
        update.message.reply_text("Пожалуйста, выбери 1 или 2.")
        return FEEDBACK

# Сохранение отзыва или предложения
def save_feedback(update: Update, context):
    user_text = update.message.text
    user_id = update.message.from_user.id
    logger.info(f"Пользователь {user_id} оставил отзыв/предложение: {user_text}")

    # Здесь можно сохранить текст в базу данных, отправить на почту или в Google Таблицы
    update.message.reply_text("Спасибо за твой вклад! Мы рассмотрим твое сообщение.")
    return ConversationHandler.END

# Отмена
def cancel(update: Update, context):
    update.message.reply_text("Диалог завершен.")
    return ConversationHandler.END

def main():
    # Вставь сюда токен своего бота
    updater = Updater("7920203645:AAFwzimpjsDflJIanMhlrWMOFkJJ0KaR0hQ", use_context=True)
    dp = updater.dispatcher

    # Обработчик диалога
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FEEDBACK: [MessageHandler(Filters.text & ~Filters.command, feedback)],
            SUGGESTION: [MessageHandler(Filters.text & ~Filters.command, save_feedback)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
