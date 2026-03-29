#!/usr/bin/env python3
import discord
import asyncio
import json
import os
import sys
import time
import random

# === ANSI ЦВЕТА ===
RED = "\033[91m"          # КРАСНЫЙ для арта
BLUE_SHADES = [
    "\033[94m",  # ярко-синий
    "\033[96m",  # циан
    "\033[34m",  # синий
    "\033[36m",  # бирюзовый
    "\033[94m",  # снова ярко-синий
]
RESET = "\033[0m"

# === КРАСНЫЙ ЭПИЧНЫЙ АРТ В НАЧАЛЕ ===
RED_ART = f"""
{RED}______________¶¶¶{RESET}
{RED}_____________¶¶_¶¶¶¶{RESET}
{RED}____________¶¶____¶¶¶{RESET}
{RED}___________¶¶¶______¶¶{RESET}
{RED}___________¶¶¶_______¶¶{RESET}
{RED}__________¶¶¶¶________¶¶{RESET}
{RED}__________¶_¶¶_________¶¶{RESET}
{RED}__________¶__¶¶_________¶¶____¶¶{RESET}
{RED}__________¶__¶¶__________¶¶¶¶¶¶¶{RESET}
{RED}_________¶¶__¶¶¶______¶¶¶¶¶¶___¶{RESET}
{RED}_________¶¶___¶¶__¶¶¶¶¶¶__¶¶{RESET}
{RED}_______¶¶_¶____¶¶¶¶________¶¶{RESET}
{RED}______¶¶__¶¶___¶¶__________¶¶{RESET}
{RED}_____¶¶____¶¶___¶¶__________¶¶{RESET}
{RED}___¶¶_______¶¶___¶¶_________¶¶{RESET}
{RED}___¶¶¶¶¶¶¶¶¶¶¶¶¶__¶¶_________¶{RESET}
{RED}_¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_¶¶________¶¶{RESET}
{RED}¶¶__¶¶¶¶¶¶____¶¶¶¶¶¶¶¶¶______¶¶{RESET}
{RED}¶¶¶¶¶___¶______¶___¶¶¶¶¶_____¶¶{RESET}
{RED}________¶¶¶¶¶¶¶¶______¶¶¶¶¶_¶¶{RESET}
{RED}______¶¶¶¶¶¶¶¶¶¶¶________¶¶¶¶{RESET}
{RED}______¶¶¶¶¶¶¶¶¶¶¶¶{RESET}
{RED}______¶__¶¶_¶¶¶¶¶¶{RESET}
{RED}_____¶¶______¶___¶{RESET}
{RED}_____¶¶_____¶¶___¶{RESET}
{RED}_____¶______¶¶___¶{RESET}
{RED}____¶¶______¶¶___¶¶{RESET}
{RED}____¶¶______¶¶___¶¶{RESET}
{RED}___¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶{RESET}
{RED}__¶¶¶¶¶¶¶¶¶_¶¶¶¶¶¶¶¶{RESET}
{RED}__¶¶________¶¶¶___{RESET}
"""

def slow_print(text, delay=0.03, use_blue=True):
    """Анимация печатающего текста (синий или обычный)"""
    for char in text:
        if use_blue:
            color = random.choice(BLUE_SHADES)
        else:
            color = RED
        sys.stdout.write(f"{color}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def rainbow_line(length=50):
    """Переливающаяся синяя линия"""
    for i in range(length):
        color = BLUE_SHADES[i % len(BLUE_SHADES)]
        sys.stdout.write(f"{color}═{RESET}")
        sys.stdout.flush()
        time.sleep(0.005)
    print()

def animated_menu():
    """Меню с анимацией"""
    rainbow_line(50)
    slow_print("   FUERT CRASH SERVER (ВАШ СЕРВЕР)", 0.02)
    rainbow_line(50)
    slow_print("1. Краш канала (массовое создание)", 0.02)
    slow_print("2. Переименовать ВСЕ каналы", 0.02)
    slow_print("3. Разослать приглашение во все каналы", 0.02)
    slow_print("4. Ввести данные заново", 0.02)
    slow_print("0. Выход", 0.02)
    rainbow_line(50)

# === КОНФИГ ===
CONFIG_FILE = "fuert_config.json"

default_config = {
    "token": "ВАШ_ТОКЕН_БОТА",
    "guild_id": "ID_ВАШЕГО_СЕРВЕРА",
    "channel_name": "FUERT FUCK",
    "spam_name": "fuck-off-niga-by-DADILK",
    "tg_link": "https://t.me/ZET_Clumsy"
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_config, f, indent=4)
        slow_print("⚙️ Создан config.json. ВСТАВЬТЕ ТОКЕН И ID СЕРВЕРА!", 0.03)
        sys.exit(1)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

config = load_config()
TOKEN = config["token"]
GUILD_ID = int(config["guild_id"])
CHANNEL_NAME = config["channel_name"]
SPAM_NAME = config["spam_name"]
TG_LINK = config["tg_link"]

def input_data():
    global CHANNEL_NAME, SPAM_NAME, TG_LINK
    slow_print("\n--- ВВОД ДАННЫХ (ПЕРЕЛИВАЮЩИЙСЯ СИНИЙ) ---", 0.02)
    CHANNEL_NAME = input(f"{BLUE_SHADES[0]}Название канала (FUERT FUCK): {RESET}") or "FUERT FUCK"
    SPAM_NAME = input(f"{BLUE_SHADES[1]}Имя для спам-каналов (fuck-off): {RESET}") or "fuck-off"
    TG_LINK = input(f"{BLUE_SHADES[2]}Telegram ссылка: {RESET}") or "https://t.me/ZET_Clumsy"
    save_config()
    slow_print("✅ Данные сохранены!", 0.03)

def save_config():
    config["channel_name"] = CHANNEL_NAME
    config["spam_name"] = SPAM_NAME
    config["tg_link"] = TG_LINK
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

async def crash_channel(guild):
    slow_print("🚨 СОЗДАЮ КАНАЛЫ...", 0.03)
    for i in range(50):
        try:
            await guild.create_text_channel(f"{SPAM_NAME}-{i}")
            slow_print(f"✅ Создан #{SPAM_NAME}-{i}", 0.01)
            await asyncio.sleep(0.5)
        except:
            slow_print("❌ Ошибка/лимит", 0.03)
    slow_print("✔️ Готово!", 0.03)

async def rename_all(guild):
    slow_print("🏷️ ПЕРЕИМЕНОВЫВАЮ КАНАЛЫ...", 0.03)
    for channel in guild.channels:
        try:
            await channel.edit(name=CHANNEL_NAME[:100])
            slow_print(f"✅ {channel.name} → {CHANNEL_NAME}", 0.01)
            await asyncio.sleep(0.5)
        except:
            pass

async def send_invite_all(guild):
    slow_print("📨 РАССЫЛАЮ ПРИГЛАШЕНИЯ...", 0.03)
    for channel in guild.text_channels:
        try:
            await channel.send(f"🔥 ПРИСОЕДИНЯЙСЯ: {TG_LINK}")
            slow_print(f"✅ Отправлено в #{channel.name}", 0.01)
            await asyncio.sleep(0.3)
        except:
            pass

class FuertBot(commands.Bot):
    async def setup_hook(self):
        slow_print(f"✅ Бот зашёл как {self.user}", 0.02)

bot = FuertBot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    # ПОКАЗЫВАЕМ КРАСНЫЙ АРТ ПРИ СТАРТЕ
    print(RED_ART)
    slow_print("\n🔥 FUERT CRASH АКТИВИРОВАН 🔥", 0.02, use_blue=False)
    
    slow_print(f"\n✅ Бот готов! Сервер: {bot.get_guild(GUILD_ID).name if bot.get_guild(GUILD_ID) else 'не найден'}", 0.02)
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        slow_print("❌ Сервер не найден! Проверьте ID в config.json", 0.03)
        await bot.close()
        return

    while True:
        animated_menu()
        choice = input(f"{BLUE_SHADES[3]}Выбор: {RESET}")
        if choice == "1":
            await crash_channel(guild)
        elif choice == "2":
            await rename_all(guild)
        elif choice == "3":
            await send_invite_all(guild)
        elif choice == "4":
            input_data()
        elif choice == "0":
            slow_print("Выход...", 0.03)
            await bot.close()
            return
        else:
            slow_print("Неверный ввод", 0.03)

if __name__ == "__main__":
    if TOKEN == "ВАШ_ТОКЕН_БОТА" or GUILD_ID == "ID_ВАШЕГО_СЕРВЕРА":
        slow_print("❌ Заполните token и guild_id в fuert_config.json!", 0.03)
    else:
        bot.run(TOKEN)
