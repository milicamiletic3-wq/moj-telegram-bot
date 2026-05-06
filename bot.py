import os
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
conversation_history = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    
    conversation_history[user_id].append({
        "role": "user",
        "content": user_message
    })
    
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        system="Ti si lični asistent. Komuniciraj na srpskom jeziku osim ako te korisnik ne zamoli drugačije. Budi koristan, koncizan i prijatan.",
        messages=conversation_history[user_id]
    )
    
    assistant_message = response.content[0].text
    
    conversation_history[user_id].append({
        "role": "assistant", 
        "content": assistant_message
    })
    
    await update.message.reply_text(assistant_message)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
