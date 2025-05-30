import os
import json
import random
import string

from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.markdown import text

from aiogram import types
from aiogram.utils.i18n import gettext as _

from routers_api import create_vpn_user, delete_vpn_user

# Token dan admin
API_TOKEN = "7216704481:AAE0Y84scLD2pVSwc9TXf7n9eJdXrjo9I7U"
ADMIN_IDS = [5988458116]

DATA_FILE = "data_pengguna.json"

# Buat Bot dan Dispatcher
bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Fungsi load dan save data
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# /start
@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "🛡️ Selamat datang di Bot VPN MURAH SUKABUMI\n\n"
        "Untuk membuat akun VPN:\n`/vpn username email`\n"
        "Contoh: `/vpn budi budi@gmail.com`\n\n"
        "Cek akun VPN:\n`/cek username`\n\n"
        "Hapus akun VPN:\n`/hapus username`\n\n"
        "Admin:\n`/list` (lihat semua user)\n\n"
        "Hubungi Admin: https://t.me/namakamu",
        parse_mode="Markdown"
    )

# /vpn
@router.message(Command("vpn"))
async def vpn_handler(message: Message):
    args = message.text.strip().split()
    if len(args) != 3:
        await message.answer("❌ Format salah.\nGunakan: `/vpn username email`", parse_mode="Markdown")
        return

    username, email = args[1], args[2]
    data = load_data()

    if username in data:
        await message.answer(f"❌ Username `{username}` sudah terdaftar.", parse_mode="Markdown")
        return

    used_ports = [int(info["port"]) for info in data.values()]
    port = max(used_ports) + 1 if used_ports else 4001
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    if create_vpn_user(username, password, port):
        data[username] = {
            "email": email,
            "password": password,
            "port": port
        }
        save_data(data)
        success_message = (
            "Akun VPN berhasil dibuat!\n\n"
            f"Username: {username}\n"
            f"Password: {password}\n"
            f"Port Winbox: {port}\n"
            f"Remote Address: {remote_address}\n"
            f"Layanan: {service}\n"
            "====================\n\n"
            "Silakan konek menggunakan Winbox atau L2TP VPN.\n"
            "Dial up - Connect To : vpnmurahsukabumi.my.id\n"
            "====================\n"
            "Layanan VPN Costum :\n"
            "Hubungi Admin: https://t.me/6285772075014\n"
            "====================\n"
            "Join Group Diskusi Usaha Internet :\n"
            "Group Telegram : Diskusi Usaha Internet"
        )
        await message.answer(success_message)

    else:
        await message.answer("❌ Gagal membuat akun VPN di MikroTik.")

# /cek
@router.message(Command("cek"))
async def cek_handler(message: Message):
    args = message.text.strip().split()
    if len(args) != 2:
        await message.answer("❌ Format salah. Gunakan: `/cek username`", parse_mode="Markdown")
        return

    username = args[1]
    data = load_data()

    if username in data:
        user = data[username]
        await message.answer(
            f"🔍 Data Akun VPN:\n"
            f"Username: `{username}`\n"
            f"Password: `{user['password']}`\n"
            f"Email: `{user['email']}`\n"
            f"Port: `{user['port']}`",
            parse_mode="Markdown"
        )
    else:
        await message.answer("❌ Username tidak ditemukan.")

# /hapus
@router.message(Command("hapus"))
async def hapus_handler(message: Message):
    args = message.text.strip().split()
    if len(args) != 2:
        await message.answer("❌ Format salah. Gunakan: `/hapus username`", parse_mode="Markdown")
        return

    username = args[1]
    data = load_data()

    if username in data:
        if delete_vpn_user(username):
            del data[username]
            save_data(data)
            await message.answer(f"✅ Akun `{username}` berhasil dihapus.", parse_mode="Markdown")
        else:
            await message.answer("❌ Gagal menghapus user di MikroTik.")
    else:
        await message.answer("❌ Username tidak ditemukan.")

# /list
@router.message(Command("list"))
async def list_handler(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ Kamu bukan admin.")
        return

    data = load_data()
    if not data:
        await message.answer("📭 Belum ada user terdaftar.")
        return

    msg = "📋 Daftar Pengguna:\n"
    for user in data:
        msg += f"- {user} ({data[user]['email']})\n"
    await message.answer(msg)

# Main app
if __name__ == "__main__":
    import asyncio

    async def main():
        print("🤖 Bot sedang berjalan...")
        await dp.start_polling(bot)

    asyncio.run(main())
