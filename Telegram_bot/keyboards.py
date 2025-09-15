from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Shaxsiy ma'lumotlar")],
        [KeyboardButton(text="Davomat ma'lumotlari"), KeyboardButton(text="Imtiyozlar")]
    ],
    resize_keyboard=True
)

benfit_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Imtiyozlarim"), KeyboardButton(text="Arizalarim")],
        [KeyboardButton(text="Faol imtiyozlar"), KeyboardButton(text="Bosh menu")]
    ],
    resize_keyboard=True
)