import telebot
from telebot import types

TOKEN = '8914326548:AAGBL9kxT13vTzeiTdRx9IwRQ3gF99Z42no'
bot = telebot.TeleBot(TOKEN)

# --- 1. CONFIGURATION & PRICING ---
rates = {'brl': 1000, 'php': 1120, 'usdt': 3500}
items_db = {
    "mlbb": {"name": "MLBB 86 Dia", "type": "T1", "currency": "BRL", "cost": 39},
    "mcgg": {"name": "MCGG 5 Dia", "type": "T1", "currency": "PHP", "cost": 5},
    "pubg": {"name": "PUBG Code", "type": "T2", "currency": "USDT", "cost": 10},
    "codm": {"name": "CODM Account", "type": "T3", "currency": "USDT", "cost": 15},
    "heart": {"name": "Heartopia", "type": "T4", "currency": "MMK", "cost": 4000}
}

def get_price(key):
    item = items_db[key]
    if item['currency'] == 'BRL': return round(((item['cost'] / 1000) * rates['brl']) * 1.10)
    if item['currency'] == 'PHP': return round(((item['cost'] / 1120) * rates['php']) * 1.10)
    if item['currency'] == 'USDT': return round((item['cost'] * rates['usdt']) * 1.10)
    return round(item['cost'] * 1.10)

# --- 2. ORDER FORMATS ---
ORDER_TEMPLATES = {
    "T1": "ID + Server\nName:\nPhone:\nUID:\nServer:\nTxnID:",
    "T2": "ID Only\nName:\nPhone:\nUID:\nTxnID:",
    "T3": "Acc\nName:\nPhone:\nMail:\nPass:\nTxnID:",
    "T4": "Code/Product\nName:\nPhone:\nProduct:\nTxnID:",
    "T5": "ငွေလဲ\nName:\nPhone:\nPay Type:\nAccount No:\nAmount:"
}

# --- 3. BOT FLOW ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    for key, val in items_db.items():
        markup.add(types.InlineKeyboardButton(f"{val['name']} ({get_price(key)} MMK)", callback_data=f"buy_{key}"))
    markup.add(types.InlineKeyboardButton("💱 ငွေလဲရန်", callback_data="buy_T5"))
    bot.send_message(message.chat.id, "ဂိမ်း/ငွေလဲ ရွေးချယ်ပါ:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def select_payment(call):
    item_key = call.data.replace('buy_', '')
    markup = types.InlineKeyboardMarkup()
    for pay in ["KBZ Pay", "Wave", "Aya", "UAB"]:
        markup.add(types.InlineKeyboardButton(pay, callback_data=f"final_{item_key}_{pay}"))
    bot.edit_message_text("ငွေပြန်လက်ခံမည့် Pay ကို ရွေးပါ:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('final_'))
def show_order_form(call):
    _, item_key, pay = call.data.split('_')
    t = "T5" if item_key == "T5" else items_db[item_key]['type']
    msg = f"ရွေးချယ်ထားသော Pay: {pay}\n\n{ORDER_TEMPLATES[t]}"
    bot.send_message(call.message.chat.id, msg)

# Admin Command (Rate ပြင်ရန်)
@bot.message_handler(commands=['setrate'])
def set_rate(message):
    bot.reply_to(message, "Rate: brl,php,usdt (ဥပမာ: /rate 1000,1120,3500)")

@bot.message_handler(commands=['rate'])
def update_rates(message):
    try:
        data = message.text.split()[1].split(',')
        rates['brl'], rates['php'], rates['usdt'] = map(float, data)
        bot.reply_to(message, "✅ Rate အသစ်များ အပ်ဒိတ်လုပ်ပြီးပါပြီ။")
    except: bot.reply_to(message, "❌ Error! Format စစ်ပါ။")

bot.polling()
