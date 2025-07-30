import logging
import os
from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

TOKEN = os.getenv("BOT_TOKEN") or "8234703289:AAGhTHudXm3SSpVZX0BK_WAbKMmE_wxI-Z0"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Дни рождения
birthdays = {
    "Гасан": "1990-11-10",
    "Гюльсум": "1994-07-06",
    "Мелек": "1996-01-04",
    "Самир": "1988-11-11",
    "Мирхади": "1990-06-02",
    "Мирза (отец)": "1960-03-05",
    "Назакат (мама)": "1964-12-01",
}

scheduler = BackgroundScheduler()
scheduler.start()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ассистент Аббаса запущен!")

def schedule_birthday_reminders(app):
    now = datetime.now()
    for name, date_str in birthdays.items():
        bday = datetime.strptime(date_str, "%Y-%m-%d")
        next_birthday = bday.replace(year=now.year)
        if next_birthday < now:
            next_birthday = next_birthday.replace(year=now.year + 1)
        remind_day = next_birthday - timedelta(days=7)
        if remind_day > now:
            scheduler.add_job(
                lambda: send_reminder(app, name, next_birthday),
                trigger=DateTrigger(run_date=remind_day),
                id=f"reminder_{name}",
                replace_existing=True
            )

def send_reminder(app, name, date):
    async def job():
        text = f"Напоминание: через 7 дней день рождения {name} ({date.strftime('%d.%m.%Y')})"
        await app.bot.send_message(chat_id=YOUR_CHAT_ID_HERE, text=text)
    app.create_task(job())

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    schedule_birthday_reminders(app)
    app.run_polling()

if _name_ == '_main_':
    main()
