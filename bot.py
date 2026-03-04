import os
import json
import logging
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# =============================
# Ambil dari Environment Variables (Railway)
TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME")
GOOGLE_CREDS_JSON = os.getenv("GOOGLE_CREDENTIALS")
# =============================

if not TOKEN:
    raise ValueError("BOT_TOKEN belum di-set di Environment Variables")

if not SPREADSHEET_NAME:
    raise ValueError("SPREADSHEET_NAME belum di-set di Environment Variables")

if not GOOGLE_CREDS_JSON:
    raise ValueError("GOOGLE_CREDENTIALS belum di-set di Environment Variables")

# Load Google Credentials dari ENV
creds_dict = json.loads(GOOGLE_CREDS_JSON)
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)
spreadsheet = client.open_by_key(19VF-vlkNkHAE_Uq6M6_BLNAIblmW3QgE88urfI2JPh4)

logging.basicConfig(level=logging.INFO)

main_menu = ReplyKeyboardMarkup(
    [
        ["📦 Masuk"],
        ["🔄 Pindahkan"],
        ["🚛 Barang Keluar"],
        ["🔍 Tracking"],
        ["📊 Cek Isi Kontainer"]
    ],
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Warehouse System Aktif ✅",
        reply_markup=main_menu
    )

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📦 Masuk":
        await update.message.reply_text("Pilih jenis: Kontainer / Box / Kerangka / Barang")
    elif text == "🔄 Pindahkan":
        await update.message.reply_text("Fitur pindahkan akan segera aktif.")
    elif text == "🚛 Barang Keluar":
        await update.message.reply_text("Fitur keluar akan segera aktif.")
    elif text == "🔍 Tracking":
        await update.message.reply_text("Ketik nomor untuk tracking.")
    elif text == "📊 Cek Isi Kontainer":
        await update.message.reply_text("Ketik nomor kontainer.")
    else:
        await update.message.reply_text("Menu tidak dikenali.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler))

print("Bot berjalan...")
app.run_polling()
