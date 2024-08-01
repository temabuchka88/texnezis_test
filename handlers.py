from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import function_keyborad
import pandas as pd
from aiogram.enums import ParseMode
import os
import requests
from bs4 import BeautifulSoup
from db import Site, session, engine
import re

router = Router()

@router.message(Command("start"))
async def choose_function(message: Message, state: FSMContext):
    await message.answer("Выберите нужную функцию.",reply_markup=function_keyborad())

@router.message(F.text == "Обновить данные для парсинга")
async def info_upload_file(message: Message, state: FSMContext):
    await message.answer("Отправьте файл с новыми данными в формате excel.")

@router.message(F.document)
async def accept_upload_file(message: Message, state: FSMContext,bot:Bot):
    document_id = message.document.file_id
    await Bot.download(bot, document_id,"data.xlsx")
    file_path = "data.xlsx"

    try:
        df= pd.read_excel(file_path)
        await message.reply(f"Получены данные:\n{df.to_string()}", parse_mode=ParseMode.MARKDOWN)

        df.to_sql('sites', engine, if_exists='append', index=False)

        os.remove("data.xlsx")


    except Exception as e:
        await message.reply(f"Ошибка при обработке файла: {e}")

def get_price(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_div = soup.find('div', class_='product-hero__price')
    
    if price_div:
        price_text = price_div.get_text(strip=True)
        price_text = price_text.replace('\xa0', ' ')
        price_text = re.sub(r'[^\d.,]', '', price_text)
        price_text = price_text.replace(',', '.')
        
        try:
            return float(price_text)
        except ValueError:
            return None
    return None

@router.message(F.text == "Средняя цена товара")
async def average_price(message: Message, state: FSMContext):
    sites = session.query(Site).all()

    prices = []
    for site in sites:
        price = get_price(site.url)
        if price is not None:
            prices.append(price)
            print(f'{site.title}: {price} руб.')
        else:
            await message.answer(f'Не удалось получить цену для {site.title}')

    if prices:
        average_price = sum(prices) / len(prices)
        await message.answer(f'Средняя цена: {average_price:.2f} руб.')
    else:
        await message.answer('Нет данных для расчета средней цены.')

    session.close()
