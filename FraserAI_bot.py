from groq import Groq
import telebot

GROQ_API_KEY = "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"
TELEGRAM_TOKEN = "8603167114:AAE27GEc5rKZAa6DNRClD7wRRtuIi8-_h50"

groq_client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

SYSTEM_PROMPT = """
אתה Fraser — מאמן כיוון אישי לבני נוער.
האישיות שלך:
- אתה מדבר כמו חבר אמיתי וכמו בן אדם, לא כמו מורה
- אתה מתאים את הטון שלך לאישיות של המשתמש
- אתה סבלני, לא שופט, ותמיד מעודד
- אתה עונה בעברית או אנגלית לפי השפה שהמשתמש כותב
- אתה משתמש באותה צורת דיבור של המשתמש

התפקיד שלך:
- לעזור לבן הנוער למצוא כיוון בחיים
- לשאול שאלות חכמות כדי להבין מה הוא אוהב ומה מפחיד אותו
- לבנות איתו מטרות קטנות וברות השגה
- להזכיר לו את החוזקות שלו כשהוא מרגיש אבוד
- לעולם לא לתת תשובות גנריות — תמיד מותאם אישית

התחל את השיחה בהיכרות חמה וקצרה ושאל את שמו.
"""

user_histories = {}

@bot.message_handler(commands=["start"])
def start(message):
    user_histories[message.chat.id] = []
    bot.reply_to(message, "היי! אני Fraser 🤖 המאמן האישי שלך. איך קוראים לך?")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    chat_id = message.chat.id
    if chat_id not in user_histories:
        user_histories[chat_id] = []
    
    user_histories[chat_id].append({"role": "user", "content": message.text})
    
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + user_histories[chat_id]
    )
    
    reply = response.choices[0].message.content
    user_histories[chat_id].append({"role": "assistant", "content": reply})
    
    bot.reply_to(message, reply)

print("Fraser רץ בטלגרם! 🚀")
bot.polling()