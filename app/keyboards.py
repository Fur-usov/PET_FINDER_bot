from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Поиск по району', callback_data='dist_search')],
    [InlineKeyboardButton(text='Поиск по цвету', callback_data='color_search')],
    [InlineKeyboardButton(text='Поиск по породе', callback_data='breed_search')],
    [InlineKeyboardButton(text='Полезные ссылки', callback_data='useful links')]
])

main_reply = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Поиск по району (чаты)'), KeyboardButton(text='Поиск по району (приюты)')],
    [KeyboardButton(text='Поиск по породе'),KeyboardButton(text='Поиск по цвету')], 
    [KeyboardButton(text='Полезные ссылки')]
], 
                                 input_field_placeholder='Выберите опцию', 
                                 resize_keyboard=True)


return_reply = ReplyKeyboardMarkup(keyboard=[ [KeyboardButton(text='меню')] ], resize_keyboard=True)

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ссылка', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')]
])


async def inline_options():
    options = []
    with open('data/options.txt', encoding='utf8') as file:
        for option in file.readlines():
            options.append(option)
            
    keyboard = InlineKeyboardBuilder()
    for opt in options:
        keyboard.add(InlineKeyboardButton(text=str(opt), url='https://youtube.com'))
    return keyboard.adjust(1).as_markup()