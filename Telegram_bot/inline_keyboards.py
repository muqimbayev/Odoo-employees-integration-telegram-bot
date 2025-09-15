from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def inline_keyboard_benefit(data):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for benefit in data['benefits']:
        btn = InlineKeyboardButton(
            text=benefit['name'],
            callback_data=f"detail:{benefit['id']}"

        )
        keyboard.inline_keyboard.append([btn])  
    return keyboard

    
def inline_keyboard_requires_approval(requires_approval: bool, benefit):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    if requires_approval:
        btn = InlineKeyboardButton(
                    text="Tasdiqlash uchun so'rov",
                    callback_data=f"confirm:{benefit}"

                )
        keyboard.inline_keyboard.append([btn]) 
    else:
        btn = InlineKeyboardButton(
                    text="Foydalanish",
                    callback_data=f"use:{benefit}"
                    

                )
        keyboard.inline_keyboard.append([btn]) 


    return keyboard
 
