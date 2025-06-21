from discord.ext import commands
import discord

import os
from dotenv import load_dotenv

from io import StringIO
from datetime import datetime, timedelta

from discord.utils import get

intents = discord.Intents.default()
intents.members = True # メンバー管理の権限
intents.message_content = True # メッセージの内容を取得する権限

# Botをインスタンス化
bot = commands.Bot(
    command_prefix=['&', '.', '/'], # &コマンド名 でコマンドを実行できるようになる
    case_insensitive=True, # コマンドの大文字小文字を区別しない（$helloも$Helloも同じ）
    intents=intents # 権限を設定
)

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.command(
    name="hello", # コマンドの名前, 設定しない場合は関数名
    aliases=["hi", "hey"] # &hiでも&heyでも反応するようになる
)
async def hello(ctx: commands.Context) -> None:
    """helloと返すコマンド"""
    await ctx.send(f"Hello {ctx.author.name}")

@bot.command()
async def add(ctx: commands.Context, a: int, b: int) -> None:
    """足し算をするコマンド"""
    await ctx.send(a+b)

@bot.command(
    name="message",
    aliases=["msg", "m"],
)
async def get_message(ctx: commands.Context, channel: discord.TextChannel) -> None:
    """チャンネルのメッセージを取得し、テキストファイルに保存するコマンド"""

    stream = StringIO() # テキストファイルのようなもの

    async for message in channel.history(
        after=datetime.utcnow() -timedelta(hours=1), # 1時間前から
        oldest_first=True, # 古い順に取得
    ):
        jst = message.created_at + timedelta(hours=9) # UTC -> JST
        msg = f"{message.author.name}: {jst.strftime('%Y/%m/%d %H:%M:%S')}\n{message.content}"
        stream.write(msg) # テキストファイルに書き込む
        stream.write("\n\n") # 改行

    stream.seek(0) # テキストファイルの先頭に戻る
    await ctx.send(file=discord.File(stream, filename="messages.txt"))
    stream.close() # テキストファイルを閉じる

@bot.command(name="mute")
async def mute(ctx: commands.Context, member: discord.Member) -> None:

    if (fole := get(member.roles, name="チャット制限")) is None: # ロールがサーバーに存在しない場合
        # ロールを作成
        role = await ctx.guild.create_role(
            name="チャット制限", # ロール名
            mentionable=True # メンションできるようにする
        )
    await member.add_roles(role) # メンバーにロールを付与
    await ctx.send(f"{member.mention} をチャット制限しました。")

@bot.event
async def on_message(message: discord.Message) -> None:

    if message.author.bot: # botからのメッセージは無視
        return

    # チャット制限ロールをメッセージ送信者が持っているか確認
    role = get(message.author.roles, name="チャット制限")

    if role is not None:
        await message.delete() # メッセージを削除
        return # ミュートされている場合はコマンドを実行しない

    await bot.process_commands(message) # コマンドを実行

# 環境変数の読み込み
load_dotenv()
TOKEN = os.getenv("TOKEN", "環境変数が設定されていません")

bot.run(TOKEN)

# @bot.event
# async def on_message(message: discord.Message):
#     """メッセージをおうむ返しする処理"""

#     if message.author.bot: # ボットのメッセージは無視
#         return

#     await message.reply(message.content)