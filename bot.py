import os
import telebot
import math
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "8914326548:AAGBL9kxT13vTzeiTdRx9IwRQ3gF99Z42no"
bot = telebot.TeleBot(TOKEN)

user_status = {}

# 💡 Smile One ရှိ ဂိမ်း (၈) ခု၏ ပုံသေ Coin/Diamond သတ်မှတ်ချက်ဇယား
# အစ်ကိုကြီးအနေဖြင့် Coin ပမာဏများကို မိမိစိတ်ကြိုက် လွတ်လပ်စွာ ပြင်ဆင်/တိုးချဲ့နိုင်ပါသည်
GAME_DATA = {
    # --- BRL REGION GAMES 🇧🇷 ---
    "MLBB_BRL": [
        ("Weekly Pass", 76.0), ("Elite Bundle", 39.0), ("Epic", 196.5),
        ("50+5 Diamonds", 39.0), ("150+15 Diamonds", 116.9), ("250+25 Diamonds", 187.5),
        ("86 Diamonds", 61.5), ("172 Diamonds", 122.0), ("706 Diamonds", 480.0),
        ("2195 Diamonds", 1453.0), ("3688 Diamonds", 2424.0), ("Twilight Pass", 402.5)
    ],
    "MCGG_BRL": [
        ("Weekly Pass", 76.0), ("100 Coins", 39.0), ("300 Coins", 116.9), ("500 Coins", 187.5)
    ],
    "PUBG_BRL": [
        ("60 UC", 39.0), ("325 UC", 196.5), ("660 UC", 393.0), ("1800 UC", 982.5)
    ],
    "WWM_BRL": [
        ("60 Crystals", 39.0), ("300 Crystals", 196.5), ("600 Crystals", 393.0)
    ],
    "BLOOD_BRL": [
        ("60 Gold", 39.0), ("330 Gold", 196.5), ("660 Gold", 393.0)
    ],
    "ARENA_BRL": [
        ("60 Bonds", 39.0), ("310 Bonds", 196.5), ("630 Bonds", 393.0)
    ],
    "RACING_BRL": [
        ("60 Gems", 39.0), ("300 Gems", 196.5), ("600 Gems", 393.0)
    ],

    # --- PHP REGION GAMES 🇵🇭 ---
    "MLBB_PHP": [
        ("Weekly Pass", 95.0), ("Elite Bundle", 47.46), ("Epic", 233.7),
        ("10 Diamonds", 9.5), ("56 Diamonds", 47.5), ("112 Diamonds", 95.0),
        ("223 Diamonds", 190.0), ("336 Diamonds", 285.0), ("570 Diamonds", 475.0),
        ("1163 Diamonds", 950.0), ("2398 Diamonds", 1900.0), ("Twilight Pass", 475.0)
    ],
    "HOK_PHP": [
        ("8 Tokens", 6.5), ("88 Tokens", 47.5), ("432 Tokens", 233.7), 
        ("896 Tokens", 475.0), ("2496 Tokens", 1187.8), ("4496 Tokens", 2138.0)
    ],
    "PUBG_PHP": [
        ("60 UC", 47.5), ("325 UC", 233.7), ("660 UC", 475.0), ("1800 UC", 1187.8)
    ],
    "BLOOD_PHP": [
        ("60 Gold", 47.5), ("330 Gold", 233.7), ("660 Gold", 475.0)
    ],
    "ARENA_PHP": [
        ("60 Bonds", 47.5), ("310 Bonds", 233.7), ("630 Bonds", 475.0)
    ]
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
    
    bot.send_message(chat_id, "👋 **Smile One Code ဈေးနှုန်းတွက်ချက်စနစ်**\n\nတွက်ချက်လိုသော Currency Region ကို ရွေးချယ်ပေးပါဗျာ။", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["set_brl", "set_php"])
def callback_listener(call):
    chat_id = call.message.chat.id
    if call.data == "set_brl":
        user_status[chat_id] = {"currency": "BRL"}
        bot.edit_message_text("✅ **Brl 🇧🇷** ကို ရွေးချယ်ပြီးပါပြီ။\n\nSmile One မှ ဝယ်ယူခဲ့သည့် **ကုဒ်ဝယ်ဈေးနှုန်း (ဂဏန်းသီးသန့်)** ကို ရိုက်ထည့်ပေးပါ။", chat_ id, call.message.message_id, parse_mode="Markdown")
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

        # 💡 ဝယ်ဈေးရိုက်ပြီးပါက Smile One ဂိမ်းများကို Inline Menu ဖြင့် ပြသခြင်း
        markup = InlineKeyboardMarkup(row_width=2)
        
        if currency == "BRL":
            markup.add(
                InlineKeyboardButton("⚔️ Mobile Legends", callback_data="main_MLBB_BRL"),
                InlineKeyboardButton("♟️ Magic Chess Go Go", callback_data="main_MCGG_BRL"),
                InlineKeyboardButton("🪂 PUBG Mobile", callback_data="main_PUBG_BRL"),
                InlineKeyboardButton("🍃 Where Winds Meet", callback_data="main_WWM_BRL"),
                InlineKeyboardButton("💥 Blood Strike", callback_data="main_BLOOD_BRL"),
                InlineKeyboardButton("📦 Arena Breakout", callback_data="main_ARENA_BRL"),
                InlineKeyboardButton("🏎️ Racing Master", callback_data="main_RACING_BRL")
            )
        else: # PHP
            markup.add(
                InlineKeyboardButton("⚔️ Mobile Legends", callback_data="main_MLBB_PHP"),
                InlineKeyboardButton("👑 Honor of Kings", callback_data="main_HOK_PHP"),
                InlineKeyboardButton("🪂 PUBG Mobile", callback_data="main_PUBG_PHP"),
                InlineKeyboardButton("💥 Blood Strike", callback_data="main_BLOOD_PHP"),
                InlineKeyboardButton("📦 Arena Breakout", callback_data="main_ARENA_PHP")
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
    
    # Smile One မူရင်း Coin ပုံသေနည်းအတိုင်း 1 Coin တန်ဖိုးတွက်ခြင်း
    if currency == "BRL":
        multiplier = price / 1000.0
        flag = "🇧🇷"
    else:
        multiplier = price / 1120.0
        flag = "🇵🇭"
        
    game_name = game_key.split("_")[0]
    
    # ဂိမ်းအမည်များကို ဖတ်ရလွယ်အောင် ပြန်ပြင်ပေးခြင်း
    name_map = {"MLBB": "Mobile Legends 💎", "MCGG": "Magic Chess Go Go ♟️", "PUBG": "PUBG Mobile 💸", "WWM": "Where Winds Meet 🍃", "BLOOD": "Blood Strike 💥", "ARENA": "Arena Breakout 📦", "RACING": "Racing Master 🏎️", "HOK": "Honor of Kings 👑"}
    display_name = name_map.get(game_name, game_name)

    title = f"{flag} **{display_name} ({currency})**\n💵 ဝယ်ဈေး: {price:,.0f} MMK\n🔢 1Coin : {multiplier:.4f} MMK\n"
    response_text = title + "━━━━━━━━━━━━━━━━━━━━\n"
    
    # ရွေးချယ်လိုက်သော ဂိမ်းတစ်ခုတည်း၏ Item များကိုသာ ဆွဲထုတ်တွက်ချက်ခြင်း
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
