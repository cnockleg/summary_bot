from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

# hours = 12
# minutes = 40

key_reply = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="/stt"), KeyboardButton(text="/buy")],
    [KeyboardButton(text="/reg"), KeyboardButton(text="/bot")],
    [KeyboardButton(text="Суммаризация (готовые периоды времени) ✨")],
    [KeyboardButton(text="Суммаризация (произвольный период времени) ✨")]
],          
            resize_keyboard=True,
            input_field_placeholder="Выбери.")

shop = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Каталог", callback_data="catalog")],
    [InlineKeyboardButton(text="Корзина", callback_data="basket")],
    [InlineKeyboardButton(text="Оплата", callback_data="pays")],
    [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])

# setting = InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text="пососать", callback_data="check_table")],
#     [InlineKeyboardButton(text="Назад", callback_data="back")]
#     ])

setting_for_buttons = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="пососать", callback_data="check_table")],
    [InlineKeyboardButton(text="Назад", callback_data="back_buttons")]])

back = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])

list = ["пшэница", "марковка", "огорец", "кортошка", "метис"]

async def list_of_smth():
    keyboard = InlineKeyboardBuilder()
    for item in list:
        keyboard.add(InlineKeyboardButton(text=item, callback_data=item))

    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_buttons"))
    return keyboard.adjust(2).as_markup()

def time_summar(hours, minutes):
    summ_time = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Часы", callback_data="hrs")],
        [InlineKeyboardButton(text="<<", callback_data="hours_minus"), InlineKeyboardButton(text=str(hours), callback_data="hours"), InlineKeyboardButton(text=">>", callback_data="hours_plus")],
        [InlineKeyboardButton(text="Минуты", callback_data="mins")],      
        [InlineKeyboardButton(text="<<", callback_data="minutes_minus"), InlineKeyboardButton(text=str(minutes), callback_data="minutes"), InlineKeyboardButton(text=">>", callback_data="minutes_plus")],
        [InlineKeyboardButton(text="Назад", callback_data="back"), InlineKeyboardButton(text="Далее", callback_data="starttime_next")]
        ])
    return summ_time

def dur_summar(minutes):
    summ_dur = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Минуты", callback_data="mins")],  
        [InlineKeyboardButton(text="<<", callback_data="super_durminutes_minus"), InlineKeyboardButton(text="<", callback_data="durminutes_minus"), 
            InlineKeyboardButton(text=str(minutes), callback_data="durminutes"), 
            InlineKeyboardButton(text=">", callback_data="durminutes_plus"), InlineKeyboardButton(text=">>", callback_data="super_durminutes_plus")],
        [InlineKeyboardButton(text="Назад", callback_data="back"), InlineKeyboardButton(text="Далее", callback_data="durtime_next")]
        ])
    return summ_dur

dates = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Сегондя", callback_data="date_today")],
    [InlineKeyboardButton(text="Вчера", callback_data="date_onedayago")],
    [InlineKeyboardButton(text="Позавчера", callback_data="date_twodayago")],
    [InlineKeyboardButton(text="Назад", callback_data="back")]
    ])

presets = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="За посл час", callback_data="last_hour"), InlineKeyboardButton(text="За этот день", callback_data="last_day")],
    [InlineKeyboardButton(text="За вчера", callback_data="yesterday")],
    [InlineKeyboardButton(text="Назад", callback_data="back")]
])