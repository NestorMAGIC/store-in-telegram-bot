START_TEXT = """
<b>Добро пожаловать в ShulkerStore!</b>

В нашем магазине ты можешь приобрести <em>лицензии майнкрафта</em> по хорошим ценам 😉

<b>У нас:</b>
<em>Быстрый сервис</em> ⏱
<em>Удобная оплата</em> 💸
<em>Отзывчивая поддержка</em> 😊
"""

SUPPORT_TEXT = """
Вы всегда можете задать любой вопрос, обратившись в нашу поддержку. Для этого напишите в чат <b>@NestorSuper</b>. Мы всегда рады вам помочь!
"""

RULES_TEXT = """
<b>Условия гарантии</b> 😊

<em>У вас украли аккаунт или логин с паролем к нему уже не подходят? Если с момента покупки прошло менее 14 дней, мы предоставим вам новый аккаунт из той же категории, обратитесь в поддержку и опишите свою проблему. Мы не останемся равнодушны 🤝</em>
"""

GUIDE_TEXT = """
<b>Гайд по входу в аккаунт</b> 😊

Вход в лицензионный аккаунт (Java Edition) осуществляется только через Microsoft, это связано с проведенной миграцией аккаунтов

<b>Как войти в аккаунт:</b>
1) <em>Скачать лаунчер с официального сайта - https://www.minecraft.net/ru-ru/download</em>
2) <em>В появившимся меню выбрать </em><b>«ВОЙТИ ЧЕРЕЗ MICROSOFT»</b>
3) <em>Пройти форму входа и наслаждаться игрой!</em>
"""

def order_text(order):

    oldprice = ''

    if order['oldprice']:
        oldprice = f'\n💵 <em>Сумма без скидки</em>: <b>{order["oldprice"]} RUB</b>'

    text = f"""
<b>Подтверждение оплаты {order['item_cat']} лицензии</b>
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖{oldprice}
💡 <em>ID заказа</em>: <b>{order['order_id']}</b>
💰 <em>Платежный шлюз</em>: <b>Юkassa</b>
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
💵 <em>Итого</em>: <b>{order['price']} RUB</b>
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
<em>У вас есть 30 минут чтобы оплатить товар, после оплаты вам предоставится доступ к аккаунту</em>    
    """
    return text

def item_text(item):

    text = f"""
    
    📋 <em>Категория товара:</em> <b>{item['cat']} лицензия</b>

💳 <em>Цена:</em> <b>{item['price']} RUB</b>

📔 <em>Описание:</em> {item['description']}

    """

    return text

def send_item(item):

    email = ''
    email_password = ''

    if item['email']:
        email = f"\n<em>Почта</em>: <b>{item['email']}</b>"
    
    if item['email_password']:
        email_password = f"\n<em>Пароль от почты</em>: <b>{item['email_password']}</b>"

    text = f"""
    <b>Вы успешно оплатили товар</b> 🥳
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
<em>Логин</em>: <b>{item['login']}</b>
<em>Пароль</em>: <b>{item['password']}</b>{email}{email_password}
➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖
<em>Спасибо за покупку, приятной игры!</em>
    """

    return text