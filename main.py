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
ONE, TWO, THREE, FOUR = range(4)
START_ROUTES, END_ROUTES = range(2)
game_continue = True


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(text="Start Game", callback_data=str(FOUR)),
        ],
        [
            InlineKeyboardButton(text="End Game", callback_data=str(ONE)),
        ],
        [
            InlineKeyboardButton(text="Statistics", callback_data=str(TWO)),
        ],
        [
            InlineKeyboardButton(text="Exit", callback_data=str(THREE)),
        ]

    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("You will regret ever starting this", reply_markup=reply_markup)
    return START_ROUTES


async def menu_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="Start Game", callback_data=str(FOUR)),
        ],
        [
            InlineKeyboardButton(text="End Game", callback_data=str(ONE)),
        ],
        [
            InlineKeyboardButton(text="Statistics", callback_data=str(TWO)),
        ],
        [
            InlineKeyboardButton(text="Exit", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="You will regret ever starting this", reply_markup=reply_markup)
    return START_ROUTES


async def begin_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    main.game_continue = True
    await query.answer()
    await query.edit_message_text(text=f"Game started")
    c = 0
    while main.game_continue:
        # if datetime.datetime.now().time() == datetime.time(6, 0, 0):
        c += 1
        if c >= 50:
            break
        fool, good = game.game()
        await Bot.send_message(chat_id=update.effective_chat.id,text=f"fool is {fool}, good is {good} today")
    keyboard = [[InlineKeyboardButton(text="Cancel", callback_data=str(THREE))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"Goodbye mothefucker. If you want to be fucked again type  - /start",
                                  reply_markup=reply_markup)
    return START_ROUTES


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Goodbye mothefucker. If you want to be fucked again type  - /start")
    return ConversationHandler.END


async def game_end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    main.game_continue = False
    await query.answer()
    await query.edit_message_text(text="Goodbye mothefucker. If you want to be fucked again type  - /start")
    return ConversationHandler.END


async def statistics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    statistic = game.get_statistics()
    message = ""
    for i in statistic.keys():
        message = message + f"{i} fool - {statistic[i]['fool']} good - {statistic[i]['good']}\n"
    keyboard = [[InlineKeyboardButton(text="Cancel", callback_data=str(TWO))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=message, reply_markup=reply_markup
    )
    return END_ROUTES


def main() -> None:
    application = Application.builder().token("5730170263:AAEtXblg63a2XWYkv3cc2NzmAlwWBRn2yPE").build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", menu)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(game_end, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(statistics, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(begin_game, pattern="^" + str(FOUR) + "$"),
            ],
            END_ROUTES: [
                CallbackQueryHandler(end, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(menu_over, pattern="^" + str(TWO) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", menu)]
    )
    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
