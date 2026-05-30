import os
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# အစ်ကို့ရဲ့ Bot Token
TOKEN = "8170909194:AAHBY2X2_cHMttxAT4qIL1UHq39eXWlhA3g"
bot = telebot.TeleBot(TOKEN)

# ယာယီ Data မှတ်မည့်နေရာ
user_status = {}

# PHP အတွက် Diamond နှင့် Coin ဇယား
PHP_DATA = [
    ("Elite Bundle", 47.46), ("Epic", 233.7), ("10 Diamonds", 9.5),
    ("20 Diamonds", 19.0), ("56 Diamonds", 47.5), ("112 Diamonds", 95.0),
    ("223 Diamonds", 190.0), ("336 Diamonds", 285.0), ("570 Diamonds", 475.0),
    ("1163 Diamonds", 950.0), ("2398 Diamonds", 1900.0), ("6042 Diamonds", 4750.0),
    ("Twilight Pass", 475.0), ("Weekly Pass", 95.0)
]

# Brl အတွက် Diamond နှင့် Coin ဇယား
BRL_DATA = [
    ("Elite Bundle", 39.0), ("Epic", 196.5), ("50+5 Diamonds", 39.0),
    ("150+15 Diamonds", 116.9), ("250+25 Diamonds", 187.5), ("500+65 Diamonds", 385.0),
    ("86 Diamonds", 61.5), ("172 Diamonds", 122.0), ("257 Diamonds", 177.5),
    ("706 Diamonds", 480.0), ("2195 Diamonds", 1453.0), ("3688 Diamonds", 2424.0),
    ("5532 Diamonds", 3660.0), ("9288 Diamonds", 6079.0), ("Twilight Pass", 402.5),
    ("Weekly Pass", 76.0)
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    if chat_id in user_status:
        del user_status[chat_id]
        
    markup = InlineKeyboardMarkup()
    btn_brl = InlineKeyboardButton("Brl 🇧🇷", callback_data="set_brl")
    btn_php = InlineKeyboardButton("PHP 🇵🇭", callback_data="set_php")
    markup.add(btn_brl, btn_php)
    
    bot.send_message(chat_id, "👋 မင်္ဂလာပါဗျာ။ Smile Code တွက်ချက်ဖို့အတွက် Currency ကို အရင်ရွေးချယ်ပေးပါရန်။", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id = call.message.chat.id
    if call.data == "set_brl":
        user_status[chat_id] = "BRL"
        bot.edit_message_text("✅ **Brl** ကို ရွေးချယ်ပြီးပါပြီ။\n\nSmile Code ဝယ်ယူခဲ့သည့် **ဈေးနှုန်း (ဂဏန်းသီးသန့်)** ကို ရိုက်ထည့်ပေးပါဗျာ။", chat_id, call.message.message_id, parse_mode="Markdown")
    elif call.data == "set_php":
        user_status[chat_id] = "PHP"
        bot.edit_message_text("✅ **PHP** ကို ရွေးချယ်ပြီးပါပြီ။\n\nSmile Code ဝယ်ယူခဲ့သည့် **ဈေးနှုန်း (ဂဏန်းသီးသန့်)** ကို ရိုက်ထည့်ပေးပါဗျာ။", chat_id, call.message.message_id, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if chat_id not in user_status:
        bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ /start ကိုနှိပ်ပြီး Currency ကို အရင်ရွေးချယ်ပေးပါဗျာ။")
        return

    try:
        price = float(text)
        if price <= 0:
            bot.reply_to(message, "⚠️ ဈေးနှုန်းက ၀ ထက်ကြီးရပါမယ်ဗျာ။")
            return

        currency = user_status[chat_id]
        if currency == "BRL":
            multiplier = price / 1000.0
            data_list = BRL_DATA
            title = f"🇧🇷 **Brl တွက်ချက်မှုရလဒ်**\n💵 ဈေးနှုန်း: {price:,.0f} MMK\n🔢 အမြှောက်ဆ: {multiplier:.4f}\n"
        else:
            multiplier = price / 1120.0
            data_list = PHP_DATA
            title = f"🇵🇭 **PHP တွက်ချက်မှုရလဒ်**\n💵 ဈေးနှုန်း: {price:,.0f} MMK\n🔢 အမြှောက်ဆ: {multiplier:.4f}\n"

                response_text = title + "━━━━━━━━━━━━━━━━━━━━\n"
        for item, coin in data_list:
            # ၁။ Coin အစား ကျသင့်မည့် မြန်မာငွေ (MMK) ကို ရှာသည်
            # (Item ရဲ့ Coin တန်ဖိုးကို အစ်ကိုရိုက်လိုက်တဲ့ ပိုက်ဆံနဲ့ မြှောက်တာပါ)
            total_mmk = coin * price  
            
            # ၂။ ရာဂဏန်းအထိ ဖြတ်ခြင်း (အနီးစပ်ဆုံး ရာပြည့်ကိန်းဖြစ်အောင် ဝိုင်းပေးခြင်း)
            # ဥပမာ - ၁၂,၃၄၅ ကျပ် ဖြစ်နေရင် ၁၂,၃၀၀ ဖြစ်သွားပါမည်
            rounded_mmk = round(total_mmk / 100) * 100
            
            # ၃။ အဖြေထုတ်မည့် စာသား (Coins အစား MMK လို့ ပြောင်းပြပါမည်)
            response_text += f"• **{item}** : {rounded_mmk:,.0f} MMK\n"
            
        response_text += "━━━━━━━━━━━━━━━━━━━━\n🔄 ထပ်မံတွက်ချက်လိုပါက /start ကို ပြန်နှိပ်နိုင်ပါတယ်ဗျာ။"

            
        response_text += "━━━━━━━━━━━━━━━━━━━━\n🔄 ထပ်မံတွက်ချက်လိုပါက /start ကို ပြန်နှိပ်နိုင်ပါတယ်ဗျာ။"
        bot.reply_to(message, response_text, parse_mode="Markdown")

    except ValueError:
        bot.reply_to(message, "❌ ကျေးဇူးပြု၍ ဂဏန်းသီးသန့်သာ ရိုက်ပို့ပေးပါဗျာ။\n(ဥပမာ - 5000)")

# အစ်ကို့ရဲ့ bot.py အောက်ဆုံး စာကြောင်းတွေကို ဒါလေးနဲ့ အစားထိုးပေးပါ
if __name__ == "__main__":
    import threading
    import http.server
    import socketserver

    # Render ရဲ့ Port Scan အမှားကို ကျော်ဖြတ်ရန် Port အတုတစ်ခု နောက်ကွယ်တွင် ဖွင့်ပေးခြင်း
    def run_dummy_server():
        port = int(os.environ.get("PORT", 5000))
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:
            httpd.serve_forever()

    # Port ဆာဗာကို Thread အဖြစ် သီးသန့်ပတ်ထားမည်
    threading.Thread(target=run_dummy_server, daemon=True).start()

    print("Bot Is Starting with Port Bypass...")
    bot.remove_webhook()
    bot.infinity_polling()

