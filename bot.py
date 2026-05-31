import telebot
from telebot import types

# အကိုပေးထားတဲ့ Token (လုံခြုံရေးအတွက် ဂရုစိုက်ပါ)
TOKEN = '8914326548:AAGBL9kxT13vTzeiTdRx9IwRQ3gF99Z42no'
bot = telebot.TeleBot(TOKEN)

# 1. Rates (Admin က /setrate နဲ့ ပြင်နိုင်သည်)
rates = {'brl': 1000, 'php': 1120, 'usdt': 3500}

# 2. Item Database (အကို့အရင်းဈေးများ)
items_db = {
    "mlbb_dia": {"name": "MLBB 86 Dia", "type": "T1", "currency": "BRL", "cost": 39},
    "mcgg_dia": {"name": "MCGG 5 Dia", "type": "T1", "currency": "PHP", "cost": 5},
    "pubg_code": {"name": "PUBG Code", "type": "T2", "currency": "USDT", "cost": 10},
    "codm_acc": {"name": "CODM Account", "type": "T3", "currency": "USDT", "cost": 15},
    "heartopia": {"name": "Heartopia", "type": "T4", "currency": "MMK", "cost": 4000}
}

# 3. ဈေးတွက်ချက်ခြင်း Logic
def get_price(key):
    item = items_db[key]
    if item['currency'] == 'BRL': return round(((item['cost'] / 1000) * rates['brl']) * 1.10)
    if item['currency'] == 'PHP': return round(((item['cost'] / 1120) * rates['php']) * 1.10)
    if item['currency'] == 'USDT': return round((item['cost'] * rates['usdt']) * 1.10)
    return round(item['cost'] * 1.10)

# 4. အော်ဒါ Format များ (Type 5 မျိုး)
ORDER_FORMATS = {
    "T1": "ID + Server\nName:\nPhone:\nUID:\nServer:\nTxnID:",
    "T2": "ID Only\nName:\nPhone:\nUID:\nTxnID:",
    "T3": "Account\nName:\nPhone:\nEmail/ID:\nPassword:\nTxnID:",
    "T4": "Code/Product\nName:\nPhone:\nProduct:\nTxnID:",
    "T5": "ငွေလဲ\nName:\nPhone:\nReceiving Pay:\nAccount No:\nAmount:"
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    for key, val in items_db.items():
        markup.add(types.InlineKeyboardButton(f"{val['name']} ({get_price(key)} MMK)", callback_data=f"buy_{key}"))
    markup.add(types.InlineKeyboardButton("💰 ငွေလဲရန်", callback_data="buy_exchange"))
    bot.send_message(message.chat.id, "ဂိမ်း/ဝန်ဆောင်မှု ရွေးချယ်ပါ:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_buy(call):
    # Payment Method ရွေးခိုင်းခြင်း
    markup = types.InlineKeyboardMarkup()
    methods = ["KBZ Pay", "Wave Money", "Aya Pay", "UAB Pay"]
    for m in methods:
        markup.add(types.InlineKeyboardButton(m, callback_data=f"format_{call.data}_{m}"))
    bot.edit_message_text("ငွေပြန်လက်ခံမည့် Pay ကို ရွေးပါ:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('format_'))
def send_format(call):
    data = call.data.split('_')
    item_key = data[2]
    pay_method = data[3]
    
    # Type ရှာခြင်း
    t_type = "T5" if item_key == "exchange" else items_db[item_key]['type']
    
    msg = f"သင်ရွေးချယ်ထားသော Pay: {pay_method}\n\n{ORDER_FORMATS[t_type]}"
    bot.send_message(call.message.chat.id, msg)

bot.polling()
