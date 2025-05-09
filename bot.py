from discord.ext import commands
import discord
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True # メンバー管理の権限
intents.message_content = True # メッセージの内容を取得する権限

# Botをインスタンス化
bot = commands.Bot(
    command_prefix="$", # $コマンド名 でコマンドを実行できるようになる
    case_insensitive=True, # コマンドの大文字小文字を区別しない（$helloも$Helloも同じ）
    intents=intents # 権限を設定
)

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.event
async def on_message(message: discord.Message):
    """メッセージをおうむ返しする処理"""

    if message.author.bot: # ボットのメッセージは無視
        return

    await message.reply(message.content)

# 環境変数の読み込み
load_dotenv()
TOKEN = os.getenv("TOKEN", "環境変数が設定されていません")

bot.run(TOKEN)