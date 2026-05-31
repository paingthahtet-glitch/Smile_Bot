import os
import telebot
import math
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8914326548:AAGBL9kxT13vTzeiTdRx9IwRQ3gF99Z42no"
bot = telebot.TeleBot(TOKEN)

user_status = {}

# 💡 Smile One ရှိ ဂိမ်းများ၏ ပုံသေ Coin/Diamond သတ်မှတ်ချက်ဇယား
GAME_DATA = {
    # --- BRL REGION GAMES 🇧🇷 ---
    "MLBB_BRL": [
        ("Weekly Pass", 76.0), ("Elite Bundle", 39.0), ("Epic Bundle", 196.5),
        ("50+5 Diamonds", 39.0), ("150+15 Diamonds", 116.9), ("250+25 Diamonds", 187.5),
        ("86 Diamonds", 61.5), ("172 Diamonds", 122.0), ("706 Diamonds", 480.0),
        ("2195 Diamonds", 1453.0), ("3688 Diamonds", 2424.0), ("Twilight Pass", 402.5)
    ],
    "MCGG_BRL": [
        ("Weekly Pass", 99.9), 
        ("Lukas Battle Reward (Lv.3)", 40.0), 
        ("Battle for Discounts (Lv.5)", 40.0),
        ("86 Diamonds", 62.5), ("172 Diamonds", 125.0), ("257 Diamonds", 187.0), 
        ("344 Diamonds", 250.0), ("516 Diamonds", 375.0), ("706 Diamonds", 500.0), 
        ("1346 Diamonds", 937.5), ("1825 Diamonds", 1250.0), ("2195 Diamonds", 1500.0), 
        ("3688 Diamonds", 2500.0), ("5532 Diamonds", 3750.0), ("9288 Diamonds", 6250.0), 
        ("Elite Bundle", 40.0), ("Epic Bundle", 40.0), ("50+5", 40.0), 
        ("150+15", 120.0), ("250+25", 200.0), ("500+65", 400.0)
    ],
    "PUBG_BRL": [
        ("60 UC", 47.9), ("325 UC", 242.0), ("660 UC", 484.4), 
        ("1800 UC", 1212.1), ("3850 UC", 2425.3), ("8100 UC", 4850.5)
    ],
    "WWM_BRL": [
        ("60 Echo Beads", 58.4), ("180 Echo Beads", 168.2), ("300 Echo Beads", 282.0),
        ("600 Echo Beads", 563.0), ("900 Echo Beads", 850.0), ("1800 Echo Beads", 1691.1),
        ("3000 Echo Beads", 2819.1), ("6000 Echo Beads", 5639.2), ("12000 Echo Beads", 11279.3),
        ("Monthly Pass", 282.0), ("Elite Battle Pass", 513.6), ("Premium Battle Pass", 958.8)
    ],
    "BLOOD_BRL": [
        ("116 Gold", 48.0), ("352 Gold", 146.0), ("594 Gold", 244.0), 
        ("1210 Gold", 489.0), ("2486 Gold", 979.0), ("6380 Gold", 2449.0)
    ],
    "HOK_BRL": [
        ("16 Tokens", 9.6), ("80 Tokens", 46.9), ("240 Tokens", 141.3), 
        ("400 Tokens", 235.7), ("560 Tokens", 330.0), ("830 Tokens", 471.3), 
        ("1245 Tokens", 707.5), ("2508 Tokens", 1415.0), ("4180 Tokens", 2358.7), 
        ("8360 Tokens", 4717.8)
    ],

    # --- PHP REGION GAMES 🇵🇭 ---
    "MLBB_PHP": [
        ("Weekly Pass", 95.0), ("Elite Bundle", 47.46), ("Epic", 233.7),
        ("10 Diamonds", 9.5), ("56 Diamonds", 47.5), ("112 Diamonds", 95.0),
        ("223 Diamonds", 190.0), ("336 Diamonds", 285.0), ("570 Diamonds", 475.0),
        ("1163 Diamonds", 950.0), ("2398 Diamonds", 1900.0), ("Twilight Pass", 475.0)
    ],
    "MCGG_PHP": [
        ("Weekly Pass", 95.0), ("Lucas", 47.45), ("Premium", 47.45),
        ("Diamond 50+5", 47.45), ("Diamond 150+15", 140.6), ("Diamond 250+25", 233.7),
        ("Diamond 500+65", 473.1), ("Diamond 5", 4.75), ("Diamond 11", 9.03),
        ("Diamond 22", 18.05), ("Diamond 56", 45.13), ("Diamond 112", 90.25),
        ("Diamond 223", 180.5), ("Diamond 339", 270.75), ("Diamond 570", 451.25),
        ("Diamond 1163", 902.5), ("Diamond 2398", 1895.0), ("Diamond 6042", 4512.5)
    ],
    "HOK_PHP": [
        ("16 Tokens", 11.69), ("80 Tokens", 59.07), ("240 Tokens", 117.82), 
        ("400 Tokens", 296.58), ("560 Tokens", 415.33), ("830 Tokens", 593.16), 
        ("1245 Tokens", 890.35), ("2508 Tokens", 1780.71), ("4180 Tokens", 2968.25), 
        ("8360 Tokens", 5937.12)
    ],
    "PUBG_PHP": [
        ("60 UC", 59.07), ("325 UC", 297.81), ("660 UC", 596.23), 
        ("1800 UC", 1491.51), ("3850 UC", 2957.18), ("8100 UC", 5914.35)
    ]
    # ✂️ Arena Breakout, Blood Strike ဒေတာများကို PHP Region မှ ဖယ်ရှားလိုက်ပါပြီ
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    if chat_id in user_status:
        del user_status[chat_id]
        
    markup = InlineKeyboardMarkup()
    btn_brl = InlineKeyboardButton("Brl 🇧🇷", callback_data="set_brl")
    btn_php = InlineKeyboardButton("PHP 🇵🇭", callback_data="set_php")
    markup.add(btn_brl, btn_php)
    
    bot.send_message(chat_id, "👋 **Smile One Code ဈေးနှုန်း**\n\nတွက်ချက်လိုသော Currency Region ကို ရွေးချယ်ပေးပါဗျာ။", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["set_brl", "set_php"])
def callback_listener(call):
    chat_id = call.message.chat.id
    if call.data == "set_brl":
        user_status[chat_id] = {"currency": "BRL"}
        bot.edit_message_text("✅ **Brl 🇧🇷** ကို ရွေးချယ်ပြီးပါပြီ။\n\nSmile One မှ ဝယ်ယူခဲ့သည့် **ကုဒ်ဝယ်ဈေးနှုန်း (ဂဏန်းသီးသန့်)** ကို ရိုက်ထည့်ပေးပါ။", chat_id, call.message.message_id, parse_mode="Markdown")
    elif call.data == "set_php":
        user_status[chat_id] = {"currency": "PHP"}
        bot.edit_message_text("✅ **PHP 🇵🇭** ကို ရွေးချယ်ပြီးပါပြီ။\n\nSmile One မှ ဝယ်ယူခဲ့သည့် **ကုဒ်ဝယ်ဈေးနှုန်း (ဂဏန်းသီးသန့်)** ကို ရိုက်ထည့်ပေးပါ။", chat_id, call.message.message_id, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id not in user_status or "currency" not in user_status[chat_id]:
        bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ /start ကိုနှိပ်ပြီး စတင်ပေးပါဗျာ။")
        return

    try:
        price = float(text)
        if price <= 0:
            bot.reply_to(message, "⚠️ ဈေးနှုန်းက ၀ ထက်ကြီးရပါမယ်ဗျာ။")
            return

        user_status[chat_id]["price"] = price
        currency = user_status[chat_id]["currency"]

        if currency == "BRL":
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("⚔️ Mobile Legends", callback_data="main_MLBB_BRL"),
                InlineKeyboardButton("♟️ Magic Chess Go Go", callback_data="main_MCGG_BRL"),
                InlineKeyboardButton("🪂 PUBG Mobile", callback_data="main_PUBG_BRL"),
                InlineKeyboardButton("🍃 Where Winds Meet", callback_data="main_WWM_BRL"),
                InlineKeyboardButton("💥 Blood Strike", callback_data="main_BLOOD_BRL"),
                InlineKeyboardButton("👑 Honor of Kings", callback_data="main_HOK_BRL")
            )
        else: # PHP (တောင်းဆိုချက်အရ ၃ ခုသာ ချန်လှပ်ထားပြီး row_width=1 ညှိပေးထားပါသည်)
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(
                InlineKeyboardButton("⚔️ Mobile Legends", callback_data="main_MLBB_PHP"),
                InlineKeyboardButton("♟️ Magic Chess Go Go", callback_data="main_MCGG_PHP"),
                InlineKeyboardButton("👑 Honor of Kings", callback_data="main_HOK_PHP"),
                InlineKeyboardButton("🪂 PUBG Mobile", callback_data="main_PUBG_PHP")
            )

        bot.send_message(chat_id, f"💵 ဝယ်ဈေး **{price:,.0f} MMK** အတွက် ဈေးနှုန်းကြည့်လိုသော **ဂိမ်းအမျိုးအစား** ကို ရွေးချယ်ပေးပါဗျာ။", reply_markup=markup)

    except ValueError:
        bot.reply_to(message, "❌ ကျေးဇူးပြု၍ ဂဏန်းသီးသန့်သာ ရိုက်ပို့ပေးပါဗျာ။\n(ဥပမာ - 55000)")

@bot.callback_query_handler(func=lambda call: call.data.startswith("main_"))
def calculate_game_price(call):
    chat_id = call.message.chat.id
    game_key = call.data.replace("main_", "") 
    
    if chat_id not in user_status or "price" not in user_status[chat_id]:
        bot.send_message(chat_id, "⚠️ သက်တမ်းကုန်ဆုံးသွားပါပြီ။ /start မှ ပြန်စတင်ပေးပါဗျာ။")
        return
        
    price = user_status[chat_id]["price"]
    currency = user_status[chat_id]["currency"]
    
    if currency == "BRL":
        multiplier = price / 1000.0
        flag = "🇧🇷"
    else:
        multiplier = price / 1120.0
        flag = "🇵🇭"
        
    game_name = game_key.split("_")[0]
    
    name_map = {"MLBB": "Mobile Legends 💎", "MCGG": "Magic Chess Go Go ♟️", "PUBG": "PUBG Mobile 💸", "WWM": "Where Winds Meet 🍃", "BLOOD": "Blood Strike 💥", "HOK": "Honor of Kings 👑"}
    display_name = name_map.get(game_name, game_name)

    title = f"{flag} **{display_name} ({currency})**\n💵 ဝယ်ဈေး: {price:,.0f} MMK\n🔢 1Coin : {multiplier:.4f} MMK\n"
    response_text = title + "━━━━━━━━━━━━━━━━━━━━\n"
    
    if game_key in GAME_DATA:
        for item, coin in GAME_DATA[game_key]:
            cost_mmk = coin * multiplier  
            selling_price = cost_mmk * 1.1 # 10% အမြတ်ပေါင်း
            rounded_mmk = math.ceil(selling_price / 100) * 100 # ရာပြည့်အပေါ်ဂဏန်း ပိုဖြတ်ခြင်း
            
            response_text += f"• **{item}** : {rounded_mmk:,.0f} MMK\n"
    else:
        response_text += "⚠️ ဤဂိမ်းအတွက် ဈေးနှုန်းဇယား မရှိသေးပါဗျာ။\n"
        
    response_text += "━━━━━━━━━━━━━━━━━━━━\n🔄 ထပ်မံတွက်ချက်လိုပါက /start ကို ပြန်နှိပ်နိုင်ပါတယ်ဗျာ။"
    
    bot.edit_message_text(response_text, chat_id, call.message.message_id, parse_mode="Markdown")
    del user_status[chat_id]

if __name__ == "__main__":
    import threading
    import http.server
    import socketserver

    def run_dummy_server():
        port = int(os.environ.get("PORT", 5000))
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
            httpd.serve_forever()

    threading.Thread(target=run_dummy_server, daemon=True).start()

    print("Bot Is Starting with Port Bypass...")
    bot.remove_webhook()
    bot.infinity_polling(timeout=60, long_polling_timeout=5)
