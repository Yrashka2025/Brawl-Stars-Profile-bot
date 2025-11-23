import telebot
import brawlstats
from telebot import types

# Tokens
telegram_token = '' # TOKEN From @BotFather
brawlstars_token = '' # Token From https://developer.brawlstars.com
# Clients
client = brawlstats.Client(brawlstars_token)
bot = telebot.TeleBot(telegram_token)

# /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📊 Send Tag"))
    bot.send_message(
        message.chat.id,
        "Hey there! 👋\nI'm your Brawl Stars stats bot.\n\n"
        "Just send me your player tag (e.g. `#ABCD1234`) and I'll show you your profile!",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# Main message handler
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()

    if text.startswith("#") and len(text) > 4:
        player_tag = text[1:].upper()

        try:
            player = client.get_player(player_tag)

            # Favorite brawler (based on highest power level)
            brawlers = player.brawlers
            if brawlers:
                favorite = max(brawlers, key=lambda b: b.power)
                fav_info = f"\n🎖️ *Favorite Brawler:* {favorite.name} (Power {favorite.power})"
            else:
                fav_info = ""

            # Updated battle stats for new versions
            response = (
                f"🔥 *Name:* {player.name}\n"
                f"🆔 *Tag:* `#{player.tag}`\n"
                f"🏆 *Trophies:* {player.trophies}\n"
                f"🥇 *Best Trophies:* {player.highest_trophies}\n"
                f"🎯 *Level:* {player.exp_level}"
                f"{fav_info}\n\n"
                f"📊 *Advanced Battle Stats:*\n"
                f"• 🎮 Wireless Victories: `{getattr(player, 'wireless_victories', 0)}`\n"
                f"• ⚔️ Solo Showdown Wins: `{player.solo_victories}`\n"
                f"• 🤝 Duo Showdown Wins: `{player.duo_victories}`\n"
                f"• 🧩 Total Victories: `{player.total_victories}`\n"
                f"• 🧠 Highest Robot Rumble Level: `{getattr(player, 'best_robot_rumble_time', 'N/A')}`\n"
                f"• 🚀 Highest Brawler Boss Fight Level: `{getattr(player, 'best_big_brawler_time', 'N/A')}`\n"
                f"• 🎯 Hit Rate: `{getattr(player, 'hit_rate', 'N/A')}%`\n"
                f"• 💥 Total Damage Dealt: `{getattr(player, 'damage', 0)}`\n"
                f"• 🔄 Total Shots Fired: `{getattr(player, 'shots', 0)}`\n"
                f"• 🏅 Evaluation Marks: `{getattr(player, 'evaluation_marks', 'N/A')}`"
            )
            bot.reply_to(message, response, parse_mode="Markdown")
        except brawlstats.NotFoundError:
            bot.reply_to(message, "❌ No player found with this tag. Please check if it's correct.")
        except Exception as e:
            bot.reply_to(message, f"⚠️ An error occurred: `{str(e)}`", parse_mode="Markdown")
    else:
        bot.reply_to(message, "Please send a valid player tag starting with `#` (e.g. `#ABCD1234`)", parse_mode="Markdown")

bot.polling()

