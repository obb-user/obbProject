import asyncio
from datetime import datetime
import os
import sys
import time

import pyautogui as pga
from aiogram import Bot, Dispatcher


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def count_white_pixels(image, tolerance=30):
    count = sum(1 for pixel in image.getdata() if all(abs(component - 255) <= tolerance for component in pixel))
    return count


def count_pixels_of_color(image, target_color, tolerance=30):
    count = sum(1 for pixel in image.getdata() if
                all(abs(component - target) <= tolerance for component, target in zip(pixel, target_color)))
    return count


async def send_telegram_message(bot, message, chat_id):
    # Отправляем сообщение
    await bot.send_message(chat_id=chat_id, text=message)


def check_mouse():
    while True:
        try:
            return pga.locateOnScreen(mouse_icon, confidence=0.75)
        except:
            pass


def click_center(mouse):
    while True:
        search_region = (int(mouse[0] - 65), int(mouse[1] - 50), mouse[2] + 30, 15)
        screenshot = pga.screenshot(region=search_region)
        total_pixels = search_region[2] * search_region[3]  # Общее количество пикселей в области
        white_pixel_count = count_white_pixels(screenshot)
        white_pixel_percentage = (white_pixel_count / total_pixels) * 100
        if white_pixel_percentage > 0:
            pga.click()
            print('Забросили')
            time.sleep(3)
            break


def check_fish():
    while True:
        try:
            screenshot = pga.screenshot(region=(875, 635, 60, 95))
            target_color = (255, 49, 49)
            pixel_count = count_pixels_of_color(screenshot, target_color)
            screen_width, screen_height = pga.size()
            total_pixels = screen_width * screen_height
            percentage = (pixel_count / total_pixels) * 100

            if percentage > 0.1:
                print('Тянем...')
                for a in range(0, 25):
                    pga.click()
                    time.sleep(0.05)
                break
        except:
            pass


def read_config(file_path):
    variables = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Удаляем пробельные символы в начале и в конце строки
                line = line.strip()
                # Пропускаем пустые строки и комментарии
                if not line or line.startswith('#'):
                    continue
                # Разделяем строку по знаку равенства
                key, value = line.split('=', 1)
                # Удаляем пробельные символы вокруг ключа и значения
                key = key.strip()
                value = value.strip()
                # Добавляем ключ и значение в словарь
                variables[key] = value
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
    return variables


async def bot(config_variables):
    TOKEN = config_variables['TOKEN']
    delay_time = int(config_variables['time'])
    message = config_variables['message']
    chat_id = config_variables['chat_id']

    bot = Bot(token=TOKEN)
    dispatcher = Dispatcher(bot)

    x = 0
    start_time = datetime.now()

    while True:
        mouse = check_mouse()
        if mouse:
            click_center(mouse)
            check_fish()
            x += 1
            print(f'Поймано {x} рыб!')

            elapsed_time = datetime.now() - start_time
            elapsed_minutes = int(elapsed_time.total_seconds() / 60)
            if elapsed_minutes > delay_time:
                await send_telegram_message(bot=bot, message=message, chat_id=chat_id)
                break


if __name__ == "__main__":
    mouse_icon = resource_path("mouse_icon.png")
    config_file = resource_path('config.txt')
    config_variables = read_config(config_file)

    asyncio.run(bot(config_variables))
