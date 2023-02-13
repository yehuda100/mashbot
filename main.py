import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

#async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def lets_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("XXX")

async def get_sign_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO handle dates and time zone section.
    #! don't forget to handle exceptions.
    #! await check for date formating.
    await update.message.reply_text("XXX")

async def get_permit_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO handle dates and time zone section.
    #! don't forget to handle exceptions.
    #! await check for date formating.
    await update.message.reply_text("XXX")

async def get_amount_payd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #! await check for amaount formating.
    await update.message.reply_text("XXX")







def main() -> None:
    application = ApplicationBuilder().token('TOKEN').build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()
    #! webhook.




if __name__ == '__main__':
    main()

#by t.me/yehuda100