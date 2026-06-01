import os
import telebot
import math
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8914326548:AAGBL9kxT13vTzeiTdRx9IwRQ3gF99Z42no"
bot = telebot.TeleBot(TOKEN)

# အသုံးပြုသူများ၏ အခြေအနေကို မှတ်တမ်းတင်ရန်
user_status = {}

# 💡 ဂိမ်းများ၏ ပုံသေ Coin/Diamond/USDT သတ်မှတ်ချက်ဇယား (နောက်ဆုံးပြင်ဆင်ပြီးစာရင်း)
GAME_DATA = {
    # --- BRL REGION GAMES 🇧🇷 ---
    "MLBB_BRL": [
        ("Weekly Pass", 76.0), ("Elite Bundle", 39.0), ("Epic Bundle", 196.5),
        ("50+5 Diamonds", 39.0), ("150+15 Diamonds", 116.9), ("250+25 Diamonds", 187.5),
        ("86 Diamonds", 61.5), ("172 Diamonds", 122.0), ("706 Diamonds", 480.0),
        ("2195 Diamonds", 1453.0), ("3688 Diamonds", 2424.0), ("Twilight Pass", 402.5)
    ],
    "MCGG_BRL": [
        ("Weekly Pass", 99.9), ("Lukas Battle Reward (Lv.3)", 40.0), ("Battle for Discounts (Lv.5)", 40.0),
        ("86 Diamonds", 62.5), ("172 Diamonds", 125.0), ("257 Diamonds", 187.0), 
        ("344 Diamonds", 250.0), ("516 Diamonds", 375.0), ("706 Diamonds", 500.0), 
        ("1346 Diamonds", 937.5), ("1825 Diamonds", 1250.0), ("2195 Diamonds", 1500.0), 
        ("3688 Diamonds", 2500.0), ("5532 Diamonds", 3750.0), ("9288 Diamonds", 6250.0), 
        ("Elite Bundle", 40.0), ("Epic Bundle", 40.0), ("50+5", 40.0), 
        ("150+15", 120.0), ("250+25", 200.0), ("500+65", 400.0)
    ],
    "HOK_BRL": [
        ("16 Tokens", 9.6), ("80 Tokens", 46.9), ("240 Tokens", 141.3), 
        ("400 Tokens", 235.7), ("560 Tokens", 330.0), ("830 Tokens", 471.3), 
        ("1245 Tokens", 707.5), ("2508 Tokens", 1415.0), ("4180 Tokens", 2358.7), 
        ("8360 Tokens", 4717.8)
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

    # --- USDT REGION GAMES 💲 ---
    "PUBG_USDT": [
        ("UC 60", 0.99), ("UC 325", 4.99), ("UC 660", 9.99),
        ("UC 1800", 24.99), ("UC 3850", 49.99), ("UC 8100", 99.99)
    ],
    "HOK_USDT": [
        ("16 Tokens", 0.20), ("80 Tokens", 0.99), ("240 Tokens", 2.99),
        ("400 Tokens", 4.99), ("560 Tokens", 6.99), ("800 +30 Tokens", 9.99),
        ("1200 +45 Tokens", 14.99), ("2400 +108 Tokens", 29.99),
        ("4000 +180 Tokens", 49.99), ("8000 + 360 Tokens", 99.99)
    ],
    "APPLE_USDT": [
        ("Apple Gift $2", 2.0), ("Apple Gift $5", 5.0), ("Apple Gift $10", 10.0),
        ("Apple Gift $20", 20.0), ("Apple Gift $50", 50.0), ("Apple Gift $100", 100.0),
        ("Apple Gift $150", 150.0), ("Apple Gift $200", 200.0), ("Apple Gift $250", 250.0),
        ("Apple Gift $300", 300.0), ("Apple Gift $350", 350.0), ("Apple Gift $400", 400.0),
        ("Apple Gift $450", 450.0), ("Apple Gift $500", 500.0)
    ],
    "S1BRL_USDT": [
        ("R$ 30 Code", 5.937), ("R$ 100 Code", 19.789), ("R$ 500 Code", 98.947),
        ("R$ 1000 Code", 197.894), ("R$ 5000 Code", 989.47)
    ],
    "S1PHP_USDT": [
        ("PHP 1120 Code", 18.161), ("PHP 5600 Code", 90.806),
        ("PHP 11200 Code", 181.612), ("PHP 56000 Code", 908.061)
    ],
    "S1RUS_USDT": [
        ("RUB 100 Code", 1.407), ("RUB 500 Code", 7.037),
        ("RUB 1000 Code", 14.074), ("RUB 5000 Code", 70.368)
    ]
}

# --- ပြန်သုံးလို့ရမယ့် Start Menu Function ---
def show_start_menu(chat_id, message_id=None):
    if chat_id in user_status:
        del user_status[chat_id]
        
    markup = InlineKeyboardMarkup(row_width=3)
    btn_brl = InlineKeyboardButton("Brl 🇧🇷", callback_data="set_brl")
    btn_php = InlineKeyboardButton("PHP 🇵🇭", callback_data="set_php")
    btn_usdt = InlineKeyboardButton("USDT 💲", callback_data="set_usdt")
    markup.add(btn_brl, btn_php, btn_usdt)
    
    text = "👋 **Smile One Code ဈေးနှုန်း**\n\nတွက်ချက်လိုသော Currency Region ကို ရွေးချယ်ပေးပါဗျာ။"
    
    if message_id:
        try:
            bot.edit_message_text(text, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception:
            bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    show_start_menu(message.chat.id)

# --- Region ခလုတ်များ ရွေးချယ်မှု Callback Listener ---
@bot.callback_query_handler(func=lambda call: call.data in ["set_brl", "set_php", "set_usdt", "back_to_start"])
def callback_regions(call):
    chat_id = call.message.chat.id
    
    if call.data == "back_to_start":
        show_start_menu(chat_id, call.message.message_id)
        return
        
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 နောက်သို့", callback_data="back_to_start"))
    
    if call.data == "set_brl":
        user_status[chat_id] = {"currency": "BRL"}
        bot.edit_message_text("✅ **Brl 🇧🇷** ကို ရွေးချယ်ပြီးပါပြီ။\n\nSmile One မှ ဝယ်ယူခဲ့သည့် **ကုဒ်ဝယ်ဈေးနှုန်း (ဂဏန်းသီးသန့်)** ကို ရိုက်ထည့်ပေးပါ။", chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "set_php":
        user_status[chat_id] = {"currency": "PHP"}
        bot.edit_message_text("✅ **PHP 🇵🇭** ကို ရွေးချယ်ပြီးပါပြီ။\n\nSmile One မှ ဝယ်ယူခဲ့သည့် **ကုဒ်ဝယ်ဈေးနှုန်း (ဂဏန်းသီးသန့်)** ကို ရိုက်ထည့်ပေးပါ။", chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "set_usdt":
        user_status[chat_id] = {"currency": "USDT"}
        bot.edit_message_text("✅ **USDT 💲** ကို ရွေးချယ်ပြီးပါပြီ။\n\nလက်ရှိပေါက်ဈေး ဖြစ်သော **USDT Rate (ဂဏန်းသီးသန့်)** ကို ရိုက်ထည့်ပေးပါ။\n(ဥပမာ - 4500)", chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

# --- ဂဏန်း/စျေးနှုန်း ရိုက်ထည့်မှုကို လက်ခံတွက်ချက်ခြင်း ---
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
            bot.reply_to(message, "⚠️ ဈေးနှုန်း/Rate သည် ၀ ထက်ကြီးရပါမယ်ဗျာ။")
            return

        user_status[chat_id]["price"] = price
        currency = user_status[chat_id]["currency"]

        back_callback = f"set_{currency.lower()}"
        
        if currency == "BRL":
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("⚔️ Mobile Legends Dia", callback_data="main_MLBB_BRL"),
                InlineKeyboardButton("♟️ Magic Chess Go Go", callback_data="main_MCGG_BRL"),
                InlineKeyboardButton("👑 Honor of Kings", callback_data="main_HOK_BRL"),
                InlineKeyboardButton("🍃 Where Winds Meet", callback_data="main_WWM_BRL"),
                InlineKeyboardButton("💥 Blood Strike", callback_data="main_BLOOD_BRL")
            )
            markup.add(InlineKeyboardButton("🔙 နောက်သို့", callback_data=back_callback))
            input_label = "ဝယ်ဈေး"
            unit = "MMK"
            
        elif currency == "PHP":
            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(
                InlineKeyboardButton("⚔️ Mobile Legends Dia", callback_data="main_MLBB_PHP"),
                InlineKeyboardButton("♟️ Magic Chess Go Go", callback_data="main_MCGG_PHP")
            )
            markup.add(InlineKeyboardButton("🔙 နောက်သို့", callback_data=back_callback))
            input_label = "ဝယ်ဈေး"
            unit = "MMK"
            
        else: # USDT
            markup = InlineKeyboardMarkup(row_width=2)
            markup.add(
                InlineKeyboardButton("🪂 PUBG UC", callback_data="main_PUBG_USDT"),
                InlineKeyboardButton("👑 Honor of Kings", callback_data="main_HOK_USDT"),
                InlineKeyboardButton("🍏 Apple Giftcard", callback_data="main_APPLE_USDT"),
                InlineKeyboardButton("🇧🇷 Smile One Brl Code", callback_data="main_S1BRL_USDT"),
                InlineKeyboardButton("🇵🇭 Smile One Php Code", callback_data="main_S1PHP_USDT"),
                InlineKeyboardButton("🇷🇺 Smile One Russia Code", callback_data="main_S1RUS_USDT")
            )
            markup.add(InlineKeyboardButton("🔙 နောက်သို့", callback_data=back_callback))
            input_label = "USDT Rate"
            unit = "ကျပ်"

        bot.send_message(chat_id, f"💵 ရိုက်ထည့်ထားသော {input_label} **{price:,.0f} {unit}** အတွက် ဈေးနှုန်းကြည့်လိုသော **ဂိမ်းအမျိုးအစား** ကို ရွေးချယ်ပေးပါဗျာ။", reply_markup=markup)

    except ValueError:
        bot.reply_to(message, "❌ ကျေးဇူးပြု၍ ဂဏန်းသီးသန့်သာ ရိုက်ပို့ပေးပါဗျာ။\n(ဥပမာ - 55000 သို့မဟုတ် 4500)")

# --- ဂိမ်းရွေးချယ်မှုအဆင့်သို့ ပြန်ဆုတ်ရန် Inline Back Key Logic ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("back_to_games_"))
def back_to_games(call):
    chat_id = call.message.chat.id
    currency = call.data.replace("back_to_games_", "").upper()
    
    if chat_id not in user_status or "price" not in user_status[chat_id]:
        show_start_menu(chat_id, call.message.message_id)
        return
        
    price = user_status[chat_id]["price"]
    back_callback = f"set_{currency.lower()}"
    
    if currency == "BRL":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("⚔️ Mobile Legends Dia", callback_data="main_MLBB_BRL"),
            InlineKeyboardButton("♟️ Magic Chess Go Go", callback_data="main_MCGG_BRL"),
            InlineKeyboardButton("👑 Honor of Kings", callback_data="main_HOK_BRL"),
            InlineKeyboardButton("🍃 Where Winds Meet", callback_data="main_WWM_BRL"),
            InlineKeyboardButton("💥 Blood Strike", callback_data="main_BLOOD_BRL")
        )
        markup.add(InlineKeyboardButton("🔙 နောက်သို့", callback_data=back_callback))
        bot.edit_message_text(f"💵 ရိုက်ထည့်ထားသော ဝယ်ဈေး **{price:,.0f} MMK** အတွက် ဈေးနှုန်းကြည့်လိုသော **ဂိမ်းအမျိုးအစား** ကို ရွေးချယ်ပေးပါဗျာ။", chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        
    elif currency == "PHP":
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("⚔️ Mobile Legends Dia", callback_data="main_MLBB_PHP"),
            InlineKeyboardButton("♟️ Magic Chess Go Go", callback_data="main_MCGG_PHP")
        )
        markup.add(InlineKeyboardButton("🔙 နောက်သို့", callback_data=back_callback))
        bot.edit_message_text(f"💵 ရိုက်ထည့်ထားသော ဝယ်ဈေး **{price:,.0f} MMK** အတွက် ဈေးနှုန်းကြည့်လိုသော **ဂိမ်းအမျိုးအစား** ကို ရွေးချယ်ပေးပါဗျာ။", chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        
    else: # USDT
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🪂 PUBG UC", callback_data="main_PUBG_USDT"),
            InlineKeyboardButton("👑 Honor of Kings", callback_data="main_HOK_USDT"),
            InlineKeyboardButton("🍏 Apple Giftcard", callback_data="main_APPLE_USDT"),
            InlineKeyboardButton("🇧🇷 Smile One Brl Code", callback_data="main_S1BRL_USDT"),
            InlineKeyboardButton("🇵🇭 Smile One Php Code", callback_data="main_S1PHP_USDT"),
            InlineKeyboardButton("🇷🇺 Smile One Russia Code", callback_data="main_S1RUS_USDT")
        )
        markup.add(InlineKeyboardButton("🔙 နောက်သို့", callback_data=back_callback))
        bot.edit_message_text(f"💵 ရိုက်ထည့်ထားသော USDT Rate **{price:,.0f} ကျပ်** အတွက် ဈေးနှုန်းကြည့်လိုသော **ဂိမ်းအမျိုးအစား** ကို ရွေးချယ်ပေးပါဗျာ။", chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

# --- အပြီးသတ် စျေးနှုန်းတွက်ချက်မှုနှင့် Output ထုတ်ပေးခြင်း ---
@bot.callback_query_handler(func=lambda call: call.data.startswith("main_"))
def calculate_game_price(call):
    chat_id = call.message.chat.id
    game_key = call.data.replace("main_", "") 
    
    if chat_id not in user_status or "price" not in user_status[chat_id]:
        bot.send_message(chat_id, "⚠️ သက်တမ်းကုန်ဆုံးသွားပါပြီ။ /start မှ ပြန်စတင်ပေးပါဗျာ။")
        return
        
    price = user_status[chat_id]["price"]
    currency = user_status[chat_id]["currency"]
    
    # Multiplier တွက်ချက်ခြင်းပုံစံ
    if currency == "BRL":
        multiplier = price / 1000.0
        flag = "🇧🇷"
        header_text = f"💵 ဝယ်ဈေး: {price:,.0f} MMK\n🔢 1Coin : {multiplier:.4f} MMK"
    elif currency == "PHP":
        multiplier = price / 1120.0
        flag = "🇵🇭"
        header_text = f"💵 ဝယ်ဈေး: {price:,.0f} MMK\n🔢 1Coin : {multiplier:.4f} MMK"
    else: # USDT
        multiplier = price # USDT Rate အတိုင်း တိုက်ရိုက်မြှောက်ပေးမည်
        flag = "💲"
        header_text = f"💵 USDT Rate: {price:,.0f} MMK"
        
    game_name = game_key.split("_")[0]
    
    name_map = {
        "MLBB": "Mobile Legends Dia ⚔️", 
        "MCGG": "Magic Chess Go Go ♟️", 
        "PUBG": "PUBG Mobile UC 🪂", 
        "WWM": "Where Winds Meet 🍃", 
        "BLOOD": "Blood Strike 💥", 
        "HOK": "Honor of Kings 👑",
        "APPLE": "Apple Giftcard 🍏",
        "S1BRL": "Smile One Brl Code 🇧🇷",
        "S1PHP": "Smile One Php Code 🇵🇭",
        "S1RUS": "Smile One Russia Code 🇷🇺"
    }
    display_name = name_map.get(game_name, game_name)

    title = f"{flag} **{display_name} ({currency})**\n{header_text}\n"
    response_text = title + "━━━━━━━━━━━━━━━━━━━━\n"
    
    if game_key in GAME_DATA:
        for item, coin in GAME_DATA[game_key]:
            cost_mmk = coin * multiplier  
            selling_price = cost_mmk * 1.1 # ၁၀% အမြတ်ပေါင်းခြင်း
            rounded_mmk = math.ceil(selling_price / 100) * 100 # ရာဂဏန်းအပေါ်ဆုံးသို့ တိုးဖြတ်ခြင်း
            
            response_text += f"• **{item}** : {rounded_mmk:,.0f} MMK\n"
    else:
        response_text += "⚠️ ဤဂိမ်းအတွက် ဈေးနှုန်းဇယား မရှိသေးပါဗျာ။\n"
        
    response_text += "━━━━━━━━━━━━━━━━━━━━\n"
    
    # ⚙️ အောက်ခြေ Inline ခလုတ်များ (ဂိမ်းပြန်ရွေးရန် နှင့် အသစ်ပြန်တွက်ရန်)
    markup = InlineKeyboardMarkup()
    btn_back = InlineKeyboardButton("🔙 ဂိမ်းပြန်ရွေးရန်", callback_data=f"back_to_games_{currency.lower()}")
    btn_start = InlineKeyboardButton("🔄 တန်ဖိုးအသစ်ပြန်တွက်ရန် (Start)", callback_data="back_to_start")
    markup.add(btn_back, btn_start)
    
    bot.edit_message_text(response_text, chat_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

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

    print("Bot Is Starting with All Updates Implemented Successfully...")
    bot.remove_webhook()
    bot.infinity_polling(timeout=60, long_polling_timeout=5)

