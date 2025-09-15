from aiogram import types
from keyboards import main_menu

async def start_handler(message: types.Message, data):
        await message.answer(f"Assalomu alaykum, {data['name']}!\nXush kelibsiz!", reply_markup=main_menu)

async def user_info(message: types.Message, data):
        text = ""
        text+=f"To'liq ism familya: {data['name']},"
        text+=f"\nTelefon raqami: {data['phone']}"
        text+=f"\nTug'ilgan sana: {data['birth_date']}"
        text+=f"\nIshga qabul qilingan sana: {data['contract_date']}"
        text+=f"\nIshlagan kunlari: {data['work_days']}"
        text+=f"\nLavozim: {data['position']}"
        text+=f"\nBo'lim: {data['department']}"
        text+=f"\nBo'lim boshlig'i: {data['department_head']}"
        await message.answer(text)



