import telebot
import instaloader
import os
import re

# 🔑 BOT TOKEN environment se
BOT_TOKEN = os.getenv("8432707587:AAFi7bR4X7SO7r8r-FI9CEJpCnE5bmyjkRk")
bot = telebot.TeleBot(BOT_TOKEN)

# 📥 Instaloader setup
L = instaloader.Instaloader(dirname_pattern="downloads", save_metadata=True)

# 🔗 Instagram link regex
insta_pattern = re.compile(r"(https?://(www\.)?instagram\.com/[^\s]+)")

# 🚀 /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "👋 Welcome to *𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗥𝗲𝗲𝗹𝘀 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗿 𝗕𝗼𝘁* 📥\n\n"
        "🔗 बस मुझे कोई भी Instagram link भेजो,\n"
        "मैं तुम्हारे लिए वो *𝗥𝗲𝗲𝗹 / 𝗩𝗶𝗱𝗲𝗼* download कर दूँगा ✅\n\n"
        "✨ साथ में *𝗖𝗮𝗽𝘁𝗶𝗼𝗻, 𝗛𝗮𝘀𝗵𝘁𝗮𝗴𝘀 और 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲* भी मिलेगा 😍",
        parse_mode="Markdown"
    )

# 📌 Instagram link handler
@bot.message_handler(func=lambda message: insta_pattern.search(message.text))
def handle_insta_link(message):
    url = insta_pattern.search(message.text).group(1)
    chat_id = message.chat.id

    msg = bot.reply_to(message, "⏳ *𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗶𝗻𝗴...* Please wait 🔥", parse_mode="Markdown")

    try:
        # 📍 Reel ka shortcode nikalna
        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # 📥 Download reel/video
        filename = f"downloads/{shortcode}.mp4"
        L.download_post(post, target="downloads")

        # 📝 Caption + hashtags + username
        caption = post.caption or "No caption"
        username = post.owner_username
        hashtags = " ".join([word for word in caption.split() if word.startswith("#")])

        bot.delete_message(chat_id, msg.message_id)

        # 🎬 Send video if exists
        if os.path.exists(filename):
            with open(filename, "rb") as video:
                bot.send_video(
                    chat_id,
                    video,
                    caption=f"👤 *𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲:* {username}\n\n📝 *𝗖𝗮𝗽𝘁𝗶𝗼𝗻:* {caption}\n\n🏷️ *𝗛𝗮𝘀𝗵𝘁𝗮𝗴𝘀:* {hashtags}",
                    parse_mode="Markdown"
                )

        # ✅ Stylish Bold Footer Message
        bot.send_message(
            chat_id,
            "⭐ 𝗜 𝗔𝗠 𝗥𝗘𝗔𝗗𝗬 𝗙𝗢𝗥 𝗬𝗢𝗨𝗥 𝗡𝗘𝗫𝗧 𝗩𝗜𝗗𝗘𝗢 ⭐\n\n"
            "📌 𝗦𝗲𝗻𝗱 𝗮 𝘃𝗮𝗹𝗶𝗱 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗥𝗲𝗲𝗹 / 𝗩𝗶𝗱𝗲𝗼 𝗟𝗶𝗻𝗸 👀\n\n"
            "[ 🤖 𝗕𝗢𝗧 𝗖𝗥𝗘𝗔𝗧𝗘𝗗 𝗕𝗬 > ー @darkvipddosx ]",
            parse_mode="Markdown"
        )

        # 🧹 Cleanup
        for f in os.listdir("downloads"):
            os.remove(os.path.join("downloads", f))

    except Exception as e:
        bot.send_message(chat_id, f"❌ *𝗘𝗿𝗿𝗼𝗿:* {e}", parse_mode="Markdown")

# 🚀 Start bot
print("🤖 Bot is running...")
bot.polling()
