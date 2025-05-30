# telegram-vpn-bot-pyhton

1. Daftar Bot Telegram untuk membuat akun VPN di MikroTik secara otomatis.
   buat di @BotFather

2. download & Install Pyhton3
   (tanya Chat GPT Untuk langkah-langkah install Pyhton)

## Cara pakai

Buka CMD untuk windows dan Terminal untuk Mac OS 

1. Install dependensi:
pip install -r requirements.txt


2. Rubah BOT TOKEN dan BOT ID Di file bot.py

3. Jalankan bot:
   python bot.py

4. Buka Telegram Bot
   Gunakan perintah /start, /vpn, /cek, dll di Telegram.


### Struktur Project

- bot.py — script utama bot  
- routers_api.py — fungsi API MikroTik  
- data_pengguna.json — penyimpanan data user (tidak disertakan di repo)  
