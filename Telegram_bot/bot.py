import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from handlers import start_handler, user_info
from inline_keyboards import inline_keyboard_benefit, inline_keyboard_requires_approval
from keyboards import benfit_keyboard, main_menu
import os
from dotenv import load_dotenv

load_dotenv()


API_TOKEN = os.getenv("API_TOKEN")
API_URL = os.getenv("API_URL")

# Bot va Dispatcher obyektlari
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Start komandasi
@dp.message(Command("start"))
async def start_info(message: types.Message):
    telegram_id = message.from_user.id 
    async with aiohttp.ClientSession() as session:
        # GET so'rov
        async with session.get(f"{API_URL}/api/user/info/{telegram_id}") as resp:
            if resp.status == 200:
                data = await resp.json()
                await start_handler(message, data)
            elif resp.status == 404:
                await message.answer(f"Sizning telegram id: {telegram_id}")
            else:
                await message.answer("API dan javob olishda xatolik!")

@dp.message(lambda msg: msg.text == "Shaxsiy ma'lumotlar")
async def get_user_info(message: types.Message):
    telegram_id = message.from_user.id
    async with aiohttp.ClientSession() as session:
        # GET so'rov
        async with session.get(f"{API_URL}/api/user/info/{telegram_id}") as resp:
            if resp.status == 200:
                data = await resp.json()
                await user_info(message, data)
            elif resp.status == 404:
                await message.answer(f"Sizning telegram id: {telegram_id}")
            else:
                await message.answer("API dan javob olishda xatolik!")

@dp.message(lambda msg: msg.text == "Imtiyozlar")
async def get_user_benefit(message: types.Message):
    await message.answer("Menulardan birini tanlang: ", reply_markup=benfit_keyboard)

@dp.message(lambda msg: msg.text == 'Bosh menu')
async def menu(message: types.Message):
    await message.answer("Menulardan birini tanlang: ", reply_markup=main_menu)


@dp.message(lambda msg: msg.text == "Imtiyozlarim")
async def get_user_benefit(message: types.Message):
    telegram_id = message.from_user.id
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/api/user/benefits/{telegram_id}") as resp:
            if resp.status == 200:
                data = await resp.json()
                await message.answer("Imtiyozlar:", reply_markup=inline_keyboard_benefit(data))
            elif resp.status == 404:
                await message.answer(f"Sizning telegram id: {telegram_id}")
            else:
                await message.answer("API dan javob olishda xatolik!")

@dp.message(lambda msg: msg.text == "Arizalarim")
async def get_user_benefit(message: types.Message):
    telegram_id = message.from_user.id
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/api/user/benefit/petition/{telegram_id}") as resp:
            if resp.status == 200:
                data = await resp.json()
                if not data['data']:
                    await message.answer("Arizalar topilmadi.")
                text = ""
                for d in data['data']:
                    if d['state'] == 'submitted':
                        text+=f"Yuborilgan: Nomi:{d['name']}, Sana: {d['date_requested']}\n\n"
                    if d['state'] == 'approved':
                        text+=f"Qabul qilingan: Nomi:{d['name']}, Sana: {d['approved_date']}\n\n"
                    if d['state'] == 'rejected':
                        text+=f"Bekor qilingan: Nomi:{d['name']}, Sabab: {d['rejection_reason']}\n\n"
                await message.answer(text)

@dp.message(lambda msg: msg.text == "Faol imtiyozlar")
async def get_user_benefit(message: types.Message):
    telegram_id = message.from_user.id
    async with aiohttp.ClientSession() as session:
        # GET so'rov
        async with session.get(f"{API_URL}/api/user/benefit/approved/{telegram_id}") as resp:
            if resp.status == 200:
                data = await resp.json()
                if not data['data']:
                    await message.answer("Faol imtiyozlar topilmadi.")
                text = ""
                for d in data['data']:
                    text+=f"Faol: Nomi:{d['name']}, Bonus turi: {d['type']}, Qabul qilingan sana: {d['approved_date']}\n\n"
                await message.answer(text)


                await message.answer("Imtiyozlar:", reply_markup=inline_keyboard_benefit(data))
            elif resp.status == 404:
                await message.answer(f"Sizning telegram id: {telegram_id}")
            else:
                await message.answer("API dan javob olishda xatolik!")

@dp.message(lambda msg: msg.text == "Davomat ma'lumotlari")
async def get_user_benefit(message: types.Message):
    telegram_id = message.from_user.id
    async with aiohttp.ClientSession() as session:
        # GET so'rov
        async with session.get(f"{API_URL}/api/user/attendance/{telegram_id}") as resp:
            if resp.status == 200:
                data = await resp.json()
                text = ""
                if data['check_in'] and data['check_out']:
                    text+=f"Kirish vaqti: {data['check_in']}\nChiqish vaqti: {data['check_out']}\nishlagan soatlari: {data['worked_hours']} \n\n"
                elif data['check_in']:
                    text+=f"Kirish vaqti: {data['check_in']}\nChiqish vaqti: ---\nishlagan soatlari: {data['worked_hours']} \n\n"
                elif data['check_out']:
                    text+=f"Kirish vaqti: ---\nChiqish vaqti: {data['check_out']}\nishlagan soatlari: {data['worked_hours']} \n\n"

                await message.answer(text)

            elif resp.status == 404:
                await message.answer(f"Sizning telegram id: {telegram_id}")
            else:
                await message.answer("API dan javob olishda xatolik!")

@dp.callback_query()
async def process_callback(callback: types.CallbackQuery):
    telegram_id = callback.from_user.id

    async with aiohttp.ClientSession() as session:
        if callback.data.startswith("detail:"):
            _, benefit_id = callback.data.split(":")
            async with session.get(f"{API_URL}/api/user/benefit/{telegram_id}/{benefit_id}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    text = (
                        f"📌 *{data['name']}*\n\n"
                        f"📝 Izoh: {data.get('note') or '-'}\n"
                        f"📂 Turi: {data['type']}\n"
                        f"💰 Foydalanish miqdori: {data.get('max_amount') or 'Cheklanmagan'}\n"
                        f"⏳ Muddati: {data['period_use']} "
                        f"{data['period_days'] if data['period_use']=='other' else ''}"
                    )
                    await callback.message.answer(
                        text, 
                        parse_mode="Markdown",
                        reply_markup=inline_keyboard_requires_approval(
                            data['requires_approval'], 
                            data['id']
                        )
                    )
                else:
                    await callback.message.answer("❌ Imtiyoz haqida ma'lumot topilmadi.")

        elif callback.data.startswith("confirm:"):
            _, benefit_id = callback.data.split(":")
            async with session.post(f"{API_URL}/api/user/benefit/{telegram_id}/{benefit_id}/confirm") as resp:
                resp_json = await resp.json()
                if resp.status == 200:
                    await callback.message.answer(f"✅ Tasdiqlash so'rovi yuborildi. Ariza raqami: {resp_json['id']}")
                    print(resp_json)
                elif resp.status == 400:
                    print(resp_json)
                    await callback.message.answer(f"Sizda yuborilgan ariza mavjud. 'Arizalarim' menyusidan ko'rishingiz mumkin. Ariza raqami: {resp_json['id']}")
                else:
                    await callback.message.answer("❌ Tasdiqlashda xato yuz berdi.")

        elif callback.data.startswith("use:"):
            _, benefit_id = callback.data.split(":")
            async with session.post(f"{API_URL}/api/user/benefit/{telegram_id}/{benefit_id}/use") as resp:
                resp_json = await resp.json()
                if resp.status == 200:
                    await callback.message.answer("✅ Foydalanish amalga oshirildi.")
                elif resp.status == 400:
                    await callback.message.answer(f"Sizda bu bonus faol.\nMa'lumot: {resp_json['approved_message']}")
                else:
                    await callback.message.answer("❌ Foydalanishda xato yuz berdi.")

    await callback.answer()



async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
