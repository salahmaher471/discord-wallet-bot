import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "wallet_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def format_million(value):
    if value >= 1_000_000:
        return f"{value/1_000_000:.2f}M"
    return str(value)

@bot.command()
async def addmoney(ctx, amount: int):
    data = load_data()
    user_id = str(ctx.author.id)
    if user_id not in data:
        data[user_id] = 0
    data[user_id] += amount * 1_000_000
    save_data(data)
    await ctx.send(f"💰 {ctx.author.name} تمت إضافة {format_million(amount * 1_000_000)} نقطة لمحفظتك. الرصيد الحالي: {format_million(data[user_id])}")

@bot.command()
async def withdraw(ctx, amount: int):
    data = load_data()
    user_id = str(ctx.author.id)
    amount_m = amount * 1_000_000
    if user_id not in data or data[user_id] < amount_m:
        await ctx.send("❌ معندكش رصيد كفاية!")
        return
    data[user_id] -= amount_m
    save_data(data)
    await ctx.send(f"💸 {ctx.author.name} سحبت {format_million(amount_m)} نقطة. الرصيد الحالي: {format_million(data[user_id])}")

@bot.command()
async def tip(ctx, member: discord.Member, amount: int):
    data = load_data()
    sender_id = str(ctx.author.id)
    receiver_id = str(member.id)
    amount_m = amount * 1_000_000

    if sender_id not in data or data[sender_id] < amount_m:
        await ctx.send("❌ معندكش رصيد كفاية علشان تبعت tip!")
        return

    if sender_id == receiver_id:
        await ctx.send("❌ مش ممكن تبعت فلوس لنفسك!")
        return

    if receiver_id not in data:
        data[receiver_id] = 0

    data[sender_id] -= amount_m
    data[receiver_id] += amount_m
    save_data(data)

    await ctx.send(f"💵 {ctx.author.name} بعت {format_million(amount_m)} نقطة لـ {member.name}. رصيدك الحالي: {format_million(data[sender_id])}")

@bot.command()
async def balance(ctx):
    data = load_data()
    user_id = str(ctx.author.id)
    bal = data.get(user_id, 0)
    await ctx.send(f"💳 {ctx.author.name} رصيدك الحالي هو: {format_million(bal)} نقطة")

@bot.event
async def on_ready():
    print(f"✅ البوت شغال كـ {bot.user}")

bot.run("MTM3NzQ1MDM5OTU2MDIzNzEwNg.Gtsyb-.xLkPG6e4Xwj_vZfY1Aikdh5fKmDDpAeVt9Keuc")
