from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove 
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

#🎮🕹▶️

from db import Database 

db = Database()

kb = ReplyKeyboardMarkup(resize_keyboard=True)
items = KeyboardButton('Товары 🏦')
support = KeyboardButton('Поддержка 👤')
rules = KeyboardButton('Гарантия ✔️')
code = KeyboardButton('Промокод ✉️')
kb.add(items)
kb.add(support, code)
kb.add(rules)

guide_ikb = InlineKeyboardMarkup(row_width=1)
guide_ikb.add(
    InlineKeyboardButton(text="Гайд по входу ▶️", callback_data="guide")
)

def cats_ikb():

    ikb = InlineKeyboardMarkup(row_width=1)
    cats = db.get_all_cat()

    for cat in cats:
        ikb.add(InlineKeyboardButton(text=f"{cat['cat']} лицензия", callback_data=cat['cat']))
    
    return ikb

def start_pay_ikb(item_id):

    ikb = InlineKeyboardMarkup(row_width=3)

    ikb.add(
        InlineKeyboardButton(text='Начать оплату ⏳', callback_data=f'start_pay:{item_id}'),
        InlineKeyboardButton(text='Назад ⬅️', callback_data='cats'),
    )
    
    return ikb    

def start_pay_back_ikb():

    ikb = InlineKeyboardMarkup(row_width=1)

    ikb.add(
        InlineKeyboardButton(text='Назад ⬅️', callback_data='cats'),
    )
    
    return ikb 

def pay_ikb(order_id):

    ikb = InlineKeyboardMarkup(row_width=2)

    ikb.add(
        InlineKeyboardButton(text='К оплате ✅', callback_data=f'pay:{order_id}'),
        InlineKeyboardButton(text='Отменить ❌', callback_data=f'remove_order:{order_id}'),
    )
    
    return ikb          
