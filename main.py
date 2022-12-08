from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)
import datetime

import data

game = data.FoolData()
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

code = ""
game_continue = True


async def begin_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main.game_continue = True
    await update.message.reply_text(text=f"Game started")
    while main.game_continue:
        if datetime.datetime.now().time() == datetime.time(6, 0, 0):
            fool, good = game.game()
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"fool is {fool}, good is {good} today")
    await update.message.reply_text(text=f"Goodbye mothefucker. If you want to be fucked again type  - /start")

async def game_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    main.game_continue = False
    return await update.message.reply_text(text="Goodbye mothefucker. If you want to be fucked again type  - /start")


async def statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    statistic = game.get_statistics()
    message = ""
    for i in statistic.keys():
        message = message + f"{i} fool - {statistic[i]['fool']} good - {statistic[i]['good']}\n"
    return await update.message.reply_text(text=message)

def main() -> None:
    application = Application.builder().token("5730170263:AAEtXblg63a2XWYkv3cc2NzmAlwWBRn2yPE").build()
    start_handler = CommandHandler("start", begin_game)
    end_handler = CommandHandler("end", game_end)
    stat_handler = CommandHandler("stat", statistics)
    application.add_handler(start_handler)
    application.add_handler(end_handler)
    application.add_handler(stat_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
