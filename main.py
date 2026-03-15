import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# TOKEN environment variable orqali olinadi
TOKEN = os.getenv("BOT_TOKEN")
print("TOKEN:", TOKEN)  # logda tokenni tekshirish uchun

# Guruh ID larini saqlash uchun set
groups = set()

# Guruhdagi xabarlarni boshqa guruhlarga yuboruvchi handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    message = update.message

    if chat.type in ["group", "supergroup"]:
        groups.add(chat.id)

        user = message.from_user.first_name
        text = message.text

        msg = f"🌍 GLOBAL CHAT\n\n👤 {user}\n💬 {text}"

        for group in groups:
            if group != chat.id:
                try:
                    await context.bot.send_message(group, msg)
                except Exception as e:
                    print(f"Xatolik: {e}")

# Botni ishga tushirish
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot ishga tushdi...")
app.run_polling()
