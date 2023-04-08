from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType

from config import *
from messages import *
from db import Database
from markups import *

import random
import time

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = Database()



# < --- Обработчик команды /start --- >



@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):

    if not db.get_user(message.from_user.id): # Регистрация нового пользователя, если его еще нет в БД
        db.add_user(message.from_user.id)

    with open('img/shulker_store.jpg', 'rb') as photo:
        await bot.send_photo(
            message.from_user.id,
            photo,
            caption=START_TEXT,
            reply_markup=kb,
            parse_mode='HTML',
        )



# < --- Обработчик любых сообщений --- >



@dp.message_handler()
async def menu_command(message: types.Message):

    spam = False

    if message.text == 'Поддержка 👤':
        await message.answer(SUPPORT_TEXT, parse_mode='HTML')
        
    elif message.text == 'Товары 🏦': 

        await bot.send_message(
            chat_id=message.from_user.id,
            text='<em>Активные категории товаров</em>',
            reply_markup=cats_ikb(),
            parse_mode='HTML',
        )

    elif message.text == 'Гарантия ✔️':
        await message.answer(text=RULES_TEXT, parse_mode='HTML')   

    elif message.text == 'Промокод ✉️' and db.get_user_code_status(message.from_user.id) == False: # Если промокода нет
        await bot.send_message(
            chat_id=message.from_user.id,
            text='<em>Введите промокод:</em>',
            parse_mode='HTML',
        )

    elif message.text == 'Промокод ✉️' and db.get_user_code_status(message.from_user.id) == True: # Если промокод есть

        user = db.get_user_by_user_id(message.from_user.id)

        await bot.send_message(
            chat_id=message.from_user.id,
            text=f'<em>К вашему профилю уже применен промокод <b>{user["code"]}</b></em>',
            parse_mode='HTML',
        )   

    # Прием промокода 

    codes = db.get_codes()

    for code in codes:
        if message.text.upper() == code['code'] and db.get_user_code_status(message.from_user.id) == False: # Если промокода нет

            db.set_code(message.from_user.id, code['code'])

            await bot.send_message(
                chat_id=message.from_user.id,
                text=f'<em>Скидка в <b>{code["discount"]}%</b> по промокоду <b>{code["code"]}</b> применена 🥰</em>',
                parse_mode='HTML',
            ) 



# < --- Обработчик для отмены оплаты --- >



@dp.callback_query_handler(text_contains='remove_order')
async def menu_callback(cb: types.CallbackQuery):

    order_id = cb.data[13:]
    order = db.get_order_by_id(order_id)

    db.delete_order(order_id)  
    db.item_in_stock(order['item_id'])

    await bot.delete_message(cb.from_user.id, cb.message.message_id)



# < --- Обработчик для начала оплаты --- >



@dp.callback_query_handler(text_contains='start_pay')
async def menu_callback(cb: types.CallbackQuery):

    item_id = cb.data[10:]
    item = db.get_item_by_id(item_id)
    user_id = cb.from_user.id
    order_id = user_id+random.randint(10001, 99999)
    item_cat = db.get_cat(item['cat'])
    price = item_cat['price']
    
    if db.get_user_code_status(user_id) == True: # Если применен промокод

        user = db.get_user_by_user_id(user_id)       
        code = db.get_code(user['code'])
        discount = code['discount']

        endprice = price - int((float(price) / 100) * discount)

    else:
        endprice = price

    db.item_in_proccess(item_id)

    order = {
        'order_id': order_id,
        'user_id': user_id, 
        'item_id': item_id,  
        'oldprice': price,              
        'price': endprice,    
        'status': 'in proccess',
        'item_cat': item['cat'],
        'lifetime': int(time.time()) + (1 * 60),        
    }

    db.add_order(
        order['order_id'], 
        order['user_id'], 
        order['item_id'],         
        order['price'], 
        order['oldprice'],
        order['status'],
        order['item_cat'],
        order['lifetime'],
    )

    await bot.send_message(
        chat_id=cb.from_user.id,
        text=order_text(order),
        parse_mode='HTML',
        reply_markup=pay_ikb(order['order_id']),
    )   



# < --- Обработчик для оплаты --- >



@dp.callback_query_handler(text_contains='pay')
async def menu_callback(cb: types.CallbackQuery):

    # Начало работы с Юкасса

    order_id = cb.data[4:]

    order = db.get_order_by_id(order_id)

    try:

        price = order['price']
        amount = str(price)+'00'

        await bot.send_invoice(
            chat_id=cb.from_user.id,
            title="ShulkerStore",
            description=f'⬇️ Оплатите товар ⬇️',
            payload=f'order_id:{order_id}',
            provider_token=YOOTOKEN,
            currency='RUB',
            start_parameter='shop',
            prices=[{
                'label': 'руб',
                'amount': int(amount),
            }],
        )

    except:
        await bot.send_message(
            chat_id=cb.from_user.id,
            text='<em>Время оплаты истекло, пожайлуста обновите заказ</em>',
            parse_mode='HTML',
        )


# Подтверждение товара

@dp.pre_checkout_query_handler()
async def proccess_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):

    order_id = pre_checkout_query['invoice_payload'][9:]

    order = db.get_order_by_id(order_id)

    try:

        if order['status'] == 'in proccess' and db.get_lifetime_status(order_id) == True: # Если товар есть
            await bot.answer_pre_checkout_query(
                pre_checkout_query.id,
                ok=True
            )
        else: # Если товара нет
            await bot.answer_pre_checkout_query(
                pre_checkout_query.id, 
                ok=False, 
                error_message='Форма недействительна - c момента оформления заказа прошло более 30 минут, пожайлуста обновите заказ'
            )
    except:
            await bot.answer_pre_checkout_query(
                pre_checkout_query.id, 
                ok=False, 
                error_message='Форма недействительна - c момента оформления заказа прошло более 30 минут, пожайлуста обновите заказ'
            )

# Оплата произведена

@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def proccess_pay(message: types.Message):

    if 'order_id' in message.successful_payment.invoice_payload:
        order_id = message.successful_payment.invoice_payload[9:]
        order = db.get_order_by_id(order_id)
        item_id = order['item_id']
        item = db.get_item_by_id(item_id)
        user = db.get_user_by_user_id(order['user_id'])

        db.complete_order(order_id)
        db.complete_item(item_id)

        if order['oldprice'] > order['price']:
            discount = order['oldprice'] - order['price']
            db.add_money_code(user['code'], discount)

        await bot.send_message(
            chat_id=message.from_user.id,
            text=send_item(item),
            parse_mode='HTML',
            reply_markup=guide_ikb,
        )



# < --- Обработчик калбэков --- >



@dp.callback_query_handler()
async def menu_callback(cb: types.CallbackQuery):
    cats = db.get_all_cat() # Все категории

    for x in range(len(cats)):
        if cb.data == cats[x]['cat']:
            await bot.delete_message(cb.from_user.id, cb.message.message_id)
            
            items = db.get_items_by_cat(cats[x]['cat']) # Все товары запрошенной категории

            if len(items) > 0:
                item = items[0]

            if items == (): # Если товара нет
                await bot.send_message(
                    chat_id=cb.from_user.id,
                    text='На данный момент в этой категории нет товаров, попробуйте позже 😔',
                    reply_markup=start_pay_back_ikb()
                )

            else: # Если товар есть

                try: # Если картинку товара удалось загрузить
                    with open(f'img/{cats[x]["img"]}', 'rb') as photo:
                        await bot.send_photo(
                            cb.from_user.id,
                            photo,
                            caption=item_text(cats[x]),
                            reply_markup=start_pay_ikb(item['id']), # Сюда item_id
                            parse_mode='HTML',
                        )
                except: # Если картинку товара не удалось загрузить
                    with open(f'img/shulker_store.jpg', 'rb') as photo: # Подставляем дефолтную картинку
                        await bot.send_photo(
                            cb.from_user.id,
                            photo,
                            caption=item_text(cats[x]),
                            reply_markup=start_pay_ikb(item['id']), # Сюда item_id
                            parse_mode='HTML',
                        )                   
    
    if cb.data == 'cats': # Назад ко всем категориям
        await bot.delete_message(cb.from_user.id, cb.message.message_id)

        await bot.send_message(
            chat_id=cb.from_user.id,
            text='<em>Активные категории товаров</em>',
            reply_markup=cats_ikb(),
            parse_mode='HTML',
        ) 

    if cb.data == 'guide': # Назад ко всем категориям

        await bot.send_message(
            chat_id=cb.from_user.id,
            text=GUIDE_TEXT,
            parse_mode='HTML',
        ) 



# < --- Запуск --- >



if __name__ == '__main__':
    executor.start_polling(
        dp,
        skip_updates=True
    )
