import pandas as pd
from datetime import date, datetime, timedelta
import os
from telegram import (InlineKeyboardButton
                    , InlineKeyboardMarkup
                    , Update
                    ,)
from telegram.ext import (ApplicationBuilder
                    , CallbackQueryHandler
                    , CommandHandler
                    , ContextTypes
                    , ConversationHandler
                    , ChatJoinRequestHandler
                    ,)
# Stages
START_ROUTES, END_ROUTES = range(2)
# Callback data
ONE, TWO, THREE = range(3)

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
# check join request available
    if update.chat_join_request:
        chat_join_request = update.chat_join_request
        user = chat_join_request.from_user
        id_tg = user.id
        name_f = user.first_name
        name_l = user.last_name if user.last_name else ""
        invite_link = chat_join_request.invite_link.name

        if user.is_bot:
            await context.bot.decline_chat_join_request(chat_join_request.chat.id, user.id)
            tg_status = 'decline'
            new_entry = {
                'id_link': invite_link,
                'id_tg': id_tg,
                'tg_f_name': name_f,
                'tg_l_name': name_l,
                'dt_tg_responde': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # current date & time
                'tg_responde_status': tg_status
            }
            await fill_join(new_entry)
        else:
            await context.bot.approve_chat_join_request(chat_join_request.chat.id, user.id)
            tg_status = 'approve'
            new_entry = {
                'id_link': invite_link,
                'id_tg': id_tg,
                'tg_f_name': name_f,
                'tg_l_name': name_l,
                'dt_tg_responde': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # current date & time
                'tg_responde_status': tg_status
            }
            await fill_join(new_entry)

 # fill user info
async def fill_join(new_entry):

    # df_respond = pd.read_csv('~/Desktop/tg_repo/responde_data.txt', sep='\t')
    df_respond = pd.read_csv(os.path.join(os.path.dirname(__file__), 'tg_repo (copy)', 'responde_data.txt'), sep='\t')
    df_respond = df_respond._append(new_entry, ignore_index=True)
    # df_respond.to_csv(os.path.expanduser('~/Desktop/tg_repo/responde_data.txt'), sep='\t', index=False)
    df_respond.to_csv(os.path.join(os.path.dirname(__file__), 'tg_repo (copy)', 'responde_data.txt'), sep='\t', index=False)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    user = update.message.from_user
    keyboard = [
        [
            InlineKeyboardButton("Terms and conditions️⚠️", callback_data=str(ONE))],
        [InlineKeyboardButton("Get report📤", callback_data=str(TWO)),
         ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f'Hi 👋,{user.first_name}! U got📧 some promo stuff📈 not long ago📆'
                                    f' so here some main course💎. Check details👀 or carry🛒 immediately as u like',
                                    reply_markup=reply_markup)
    return START_ROUTES

async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE))],
           [InlineKeyboardButton("2", callback_data=str(TWO)),
         ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Start handler, Choose a route", reply_markup=reply_markup)
    return START_ROUTES

async def one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Sure it's clear(stay)", callback_data=str(TWO)),
            InlineKeyboardButton("No it's scares(leave)", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='⚠️'"Exposed information is opensource based. So any interpretations about data is your own risk. "
             "All what we have about data is trivial🧮 and common data execution methods📊 to convenient exhibition."'🍬'
             "So try to be prudent in your conclusions and please warn us 📩 if you catch🔍 some data inconsistency."
             "Regards!"'😎', reply_markup=reply_markup
    )
    return START_ROUTES

async def two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    chat_id = update.effective_chat.id  # chat id extraction
    document_path = os.path.expanduser('~/Desktop/key_bb.txt')  # file path
    await context.bot.send_document(chat_id=chat_id, caption='as we`ve told before here is your report📊',document=open(document_path, 'rb'))
    return END_ROUTES

async def three(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="So it was a flee meet🤷. Hope u not upsat and we'll see u soon👋!")
    return ConversationHandler.END

def main() -> None:
# upload main params
    df = pd.read_csv('~/Desktop/key_b.txt', header=None) # HIDE WHEN 127 FILLED PROPER
    bot_token = df.iloc[0, 0] # move df.iloc[0, 0] and ADD HERE 'YOUR_BOT_TOKEN' instead

# app create set main params
    application = ApplicationBuilder().token(bot_token).build()
# hand join request
    application.add_handler(ChatJoinRequestHandler(callback))
# hand bot chatting
    conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                START_ROUTES: [
                    CallbackQueryHandler(one, pattern="^" + str(ONE) + "$"),
                    CallbackQueryHandler(two, pattern="^" + str(TWO) + "$"),
                    CallbackQueryHandler(three, pattern="^" + str(THREE) + "$"),
                    # CallbackQueryHandler(four, pattern="^" + str(FOUR) + "$"),
                ],
                END_ROUTES: [
                    CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
                    # CallbackQueryHandler(end, pattern="^" + str(TWO) + "$"),
                ],
            },
            fallbacks=[CommandHandler("start", start)],
        )
# Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))

# setup call
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()