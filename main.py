#!/usr/bin/env python3
import discord
from discord.ext import commands
import asyncio
import json
import os
import sys
import time
import random

# === ANSI ЦВЕТА ===
RED = "\033[91m"
BLUE_SHADES = ["\033[94m", "\033[96m", "\033[34m", "\033[36m", "\033[94m"]
RESET = "\033[0m"

# === КРАСНЫЙ ЭПИЧНЫЙ АРТ ===
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
    for char in text:
        color = random.choice(BLUE_SHADES) if use_blue else RED
        sys.stdout.write(f"{color}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def rainbow_line(length=50):
    for i in range(length):
        color = BLUE_SHADES[i % len(BLUE_SHADES)]
        sys.stdout.write(f"{color}═{RESET}")
        sys.stdout.flush()
        time.sleep(0.005)
    print()

def animated_menu():
    rainbow_line(50)
    slow_print("   FUERT CRASH SERVER (ВАШ СЕРВЕР)", 0.02)
    rainbow_line(50)
    slow_print("1. Краш канала (массовое создание)", 0.02)
    slow_print("2. Переименовать ВСЕ каналы", 0.02)
    slow_print("3. Разослать приглашение во все каналы", 0.02)
    slow_print("4. Ввести данные (токен и ID сервера)", 0.02)
    slow_print("5. Изменить названия / ссылку", 0.02)
    slow_print("0. Выход", 0.02)
    rainbow_line(50)

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

def input_bot_data():
    slow_print("\n--- ВВОД ТОКЕНА И ID СЕРВЕРА ---", 0.02)
    token = input(f"{BLUE_SHADES[0]}Токен бота: {RESET}")
    guild_id = input(f"{BLUE_SHADES[1]}ID сервера: {RESET}")
    return token, guild_id

def input_custom_data():
    global channel_name, spam_name, tg_link
    slow_print("\n--- ИЗМЕНЕНИЕ НАЗВАНИЙ И ССЫЛКИ ---", 0.02)
    channel_name = input(f"{BLUE_SHADES[0]}Название канала (FUERT FUCK): {RESET}") or "FUERT FUCK"
    spam_name = input(f"{BLUE_SHADES[1]}Имя спам-каналов (fuck-off): {RESET}") or "fuck-off-niga-by-DADILK"
    tg_link = input(f"{BLUE_SHADES[2]}Telegram ссылка: {RESET}") or "https://t.me/ZET_Clumsy"
    config = load_config()
    config["channel_name"] = channel_name
    config["spam_name"] = spam_name
    config["tg_link"] = tg_link
    save_config(config)
    slow_print("✅ Данные сохранены!", 0.03)

# === ОСНОВНАЯ ФУНКЦИЯ ===
async def main():
    print(RED_ART)
    slow_print("🔥 FUERT CRASH ДЛЯ ВАШЕГО СЕРВЕРА 🔥", 0.02, use_blue=False)
    
    config = load_config()
    
    token = config["token"]
    guild_id = config["guild_id"]
    channel_name = config["channel_name"]
    spam_name = config["spam_name"]
    tg_link = config["tg_link"]
    
    bot = None
    guild = None
    
    while True:
        animated_menu()
        choice = input(f"{BLUE_SHADES[3]}Выбор: {RESET}")
        
        if choice == "1":
            if not token or not guild_id:
                slow_print("❌ Сначала введите токен и ID сервера (пункт 4)", 0.03)
                continue
            if bot is None or not bot.is_ready():
                slow_print("⏳ Подключаю бота...", 0.02)
                bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
                
                @bot.event
                async def on_ready():
                    nonlocal guild
                    guild = bot.get_guild(int(guild_id))
                    slow_print(f"✅ Бот {bot.user} подключён!", 0.02)
                
                try:
                    await bot.start(token)
                except Exception as e:
                    slow_print(f"❌ Ошибка: {e}", 0.03)
                    bot = None
                    continue
            
            if guild is None:
                guild = bot.get_guild(int(guild_id))
                if guild is None:
                    slow_print("❌ Сервер не найден! Проверьте ID", 0.03)
                    continue
            
            slow_print("🚨 СОЗДАЮ КАНАЛЫ...", 0.03)
            for i in range(50):
                try:
                    await guild.create_text_channel(f"{spam_name}-{i}")
                    slow_print(f"✅ Создан #{spam_name}-{i}", 0.01)
                    await asyncio.sleep(0.5)
                except:
                    slow_print("❌ Ошибка/лимит", 0.03)
            slow_print("✔️ Готово!", 0.03)
        
        elif choice == "2":
            if not token or not guild_id:
                slow_print("❌ Сначала введите токен и ID сервера (пункт 4)", 0.03)
                continue
            if bot is None or not bot.is_ready():
                slow_print("⏳ Подключаю бота...", 0.02)
                bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
                
                @bot.event
                async def on_ready():
                    nonlocal guild
                    guild = bot.get_guild(int(guild_id))
                    slow_print(f"✅ Бот {bot.user} подключён!", 0.02)
                
                try:
                    await bot.start(token)
                except Exception as e:
                    slow_print(f"❌ Ошибка: {e}", 0.03)
                    bot = None
                    continue
            
            if guild is None:
                guild = bot.get_guild(int(guild_id))
                if guild is None:
                    slow_print("❌ Сервер не найден! Проверьте ID", 0.03)
                    continue
            
            slow_print("🏷️ ПЕРЕИМЕНОВЫВАЮ КАНАЛЫ...", 0.03)
            for channel in guild.channels:
                try:
                    await channel.edit(name=channel_name[:100])
                    slow_print(f"✅ {channel.name} → {channel_name}", 0.01)
                    await asyncio.sleep(0.5)
                except:
                    pass
        
        elif choice == "3":
            if not token or not guild_id:
                slow_print("❌ Сначала введите токен и ID сервера (пункт 4)", 0.03)
                continue
            if bot is None or not bot.is_ready():
                slow_print("⏳ Подключаю бота...", 0.02)
                bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
                
                @bot.event
                async def on_ready():
                    nonlocal guild
                    guild = bot.get_guild(int(guild_id))
                    slow_print(f"✅ Бот {bot.user} подключён!", 0.02)
                
                try:
                    await bot.start(token)
                except Exception as e:
                    slow_print(f"❌ Ошибка: {e}", 0.03)
                    bot = None
                    continue
            
            if guild is None:
                guild = bot.get_guild(int(guild_id))
                if guild is None:
                    slow_print("❌ Сервер не найден! Проверьте ID", 0.03)
                    continue
            
            slow_print("📨 РАССЫЛАЮ ПРИГЛАШЕНИЯ...", 0.03)
            for channel in guild.text_channels:
                try:
                    await channel.send(f"🔥 ПРИСОЕДИНЯЙСЯ: {tg_link}")
                    slow_print(f"✅ Отправлено в #{channel.name}", 0.01)
                    await asyncio.sleep(0.3)
                except:
                    pass
        
        elif choice == "4":
            token, guild_id = input_bot_data()
            config = load_config()
            config["token"] = token
            config["guild_id"] = guild_id
            save_config(config)
            if bot is not None:
                await bot.close()
                bot = None
                guild = None
            slow_print("✅ Данные сохранены! Используйте пункты 1-3", 0.03)
        
        elif choice == "5":
            input_custom_data()
            channel_name = load_config()["channel_name"]
            spam_name = load_config()["spam_name"]
            tg_link = load_config()["tg_link"]
        
        elif choice == "0":
            slow_print("Выход...", 0.03)
            if bot is not None:
                await bot.close()
            return
        
        else:
            slow_print("Неверный ввод", 0.03)

if __name__ == "__main__":
    asyncio.run(main())
