from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ExtBot, filters, Updater, Application, CommandHandler, CallbackContext, CallbackQueryHandler,MessageHandler, TypeHandler
import asyncio
from scrapesite import scrapesite
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import STATE_RUNNING, STATE_PAUSED, STATE_STOPPED
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputMediaPhoto

nachat = ReplyKeyboardMarkup(
    [
        [
            "Начать"
        ]
    ],
    resize_keyboard=True
)


domoj = ReplyKeyboardMarkup(
    [
        [
            "Приостановить"
        ]
    ],
    resize_keyboard=True
)



TOKEN = '6662020357:AAGHifJH4tcGgFvpkZif7BUn9TsZGbaMXXs'
bot = Bot(token=TOKEN)
user_id = None
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Добро пожаловать домой, мой пират. Жаждешь легкой наживы? No to prosze Pana, нажимай на меня скорее и вперед в бой!', reply_markup=nachat)
    if user_id in user_states:
        del user_states[user_id]

async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text == "Приостановить":
        await start(update, context)
        context.user_data.pop('state', None)
        if scheduler.state is STATE_RUNNING:
            scheduler.shutdown()
            context.user_data.pop('scheduler', None)

    elif text == "Начать":
        await scrape(update, context)





async def scrape(update: Update, context: CallbackContext) -> None:

    if not context.user_data.get('state'):
        context.user_data['state'] = False
    else:
        pass

    if context.user_data['state'] is not True:
        await update.message.reply_text('Если хотите приостановить работу бота, нажмите кнопку внизу экрана.', reply_markup=domoj)
        context.user_data['state'] = True




    user_id = update.message.chat_id
    user_states[user_id] = True

    await scrape_update()


user_states = {}



async def scrape_update():
    for user_id in user_states:
        item = scrapesite()
        if item is not None:
            if item['image']:
                # There are images to send
                 # Limit to 10 images
                text = f"Название объявления: {item['Nazwa']}\nЦена: {item['Cena']}\nСтатус о торге: {item['Negocjacja']}\nОтправка почтой: {item['Wysylka']}\nГород продавца: {item['Miasto']}\nПамять устройства: {item['Pamiec']}\nСостояние: {item['Stan']}\nСсылка: {item['Url']}\nОписание: {item['Opis']}"
                media_group = []

                for num, url in enumerate(item['image'][:9]):
                    if num == 0:
                        media_group.append(InputMediaPhoto(media=url, caption=text[:1024]))
                    else:
                        media_group.append(InputMediaPhoto(media=url))
                # Send the media group
                await bot.send_media_group(chat_id=user_id, media=media_group)
                if scheduler.state is not STATE_RUNNING:
                    scheduler.start()
            else:
                # No images available, send a text message instead
                message_text = f"Название объявления: {item['Nazwa']}\nЦена: {item['Cena']}\nСтатус о торге: {item['Negocjacja']}\nОтправка почтой: {item['Wysylka']}\nГород продавца: {item['Miasto']}\nПамять устройства: {item['Pamiec']}\nСостояние: {item['Stan']}\nСсылка: {item['Url']}\nОписание: {item['Opis']}"
                await bot.send_message(chat_id=user_id, text=message_text)
                if scheduler.state is not STATE_RUNNING:
                    scheduler.start()
        else:
            break
    # Optionally log the issue or notify the user
    # Do not break the loop to continue attempting updates for other users


scheduler = AsyncIOScheduler(event_loop=asyncio.get_event_loop())
scheduler.add_job(scrape_update, 'interval', minutes=1)






def main() -> None:
    # Create an Application instance with your bot token
    application = Application.builder().token(TOKEN).build()

    # Add a CommandHandler for the /start command and link it to the start function
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters=(filters.TEXT & ~filters.COMMAND), callback=handle_message))


    # Start the bot and run it until it's stopped
    application.run_polling(timeout=0.5)  # Или укажите другой интервал опроса

    asyncio.get_event_loop().run_forever()

# Ensure that the script is being run directly and not imported as a module
if __name__ == '__main__':
    asyncio.run(main())
