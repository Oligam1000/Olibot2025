import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 8015192537

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📸 Send Payment Screenshot", callback_data='register')],
        [InlineKeyboardButton("🎓 Batch of 2016", url="https://t.me/+40BJbpajIQw3NDQ0")],
        [InlineKeyboardButton("📩 Contact Admin", url="https://t.me/Oligam1000")]
    ]
    await update.message.reply_text(
        "👑 *Welcome to OLIGAM WORLD!*

Please register by sending your payment screenshot.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    file_id = update.message.photo[-1].file_id
    keyboard = [
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
        ]
    ]
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=file_id,
        caption=f"New Registration:\nName: {user.full_name}\nUsername: @{user.username or 'N/A'}\nUserID: {user.id}",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    await update.message.reply_text("✅ Your screenshot has been sent for approval.")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    action, user_id = query.data.split("_")
    await query.answer()
    if action == "approve":
        await context.bot.send_message(chat_id=int(user_id), text="✅ Approved by admin.")
        await query.edit_message_caption(caption="✅ Approved")
    elif action == "reject":
        await context.bot.send_message(chat_id=int(user_id), text="❌ Rejected by admin.")
        await query.edit_message_caption(caption="❌ Rejected")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    await app.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())