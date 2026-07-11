import discord
from discord.ext import commands
import asyncio
import os
import sqlite3
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- Ayarlar ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot aktif!"
def run_web(): app.run(host='0.0.0.0', port=8080)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Yapay Zeka Ayarı
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

spam_aktif = False
silme_aktif = False

# --- Veritabanı ---
def init_db():
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS uyari (user_id INTEGER, sayi INTEGER)')
    conn.commit()
    conn.close()

# --- Komutlar ---
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!yardım"))
    print(f'Bot hazır: {bot.user}')

@bot.command()
async def sor(ctx, *, soru):
    """Yapay zekaya soru sorar."""
    async with ctx.typing():
        try:
            response = model.generate_content(soru)
            await ctx.send(response.text)
        except Exception as e:
            await ctx.send("Hata: API anahtarını kontrol et veya tekrar dene.")

@bot.command()
async def valdo(ctx): await ctx.send("YARRAMM VALDO BU KIM AMK")
@bot.command()
async def gonu(ctx): await ctx.send("2 GUNDE 48 CK ATAN ADAM")
@bot.command()
async def eternal(ctx): await ctx.send("FURKANIN NAMIDEGER BABASI")
@bot.command()
async def klowinc(ctx): await ctx.send("BU ADAMIN TASSAKLARINA BETON YETMEZ")
@bot.command()
async def doruk(ctx): await ctx.send("ARİEL BABAAAA")

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.name} banlandı!')

import discord
from discord.ext import commands
import asyncio
import os
import sqlite3
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- Ayarlar ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot aktif!"
def run_web(): app.run(host='0.0.0.0', port=8080)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

spam_aktif = False

# --- Veritabanı ---
def init_db():
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS uyari (user_id INTEGER, sayi INTEGER)')
    conn.commit()
    conn.close()

# --- Komutlar ---
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!yardım"))
    print(f'Bot hazır: {bot.user}')

@bot.command()
async def sor(ctx, *, soru):
    """Yapay zekaya soru sorar."""
    async with ctx.typing():
        try:
            # Anahtarı ve modeli her seferinde güvenli şekilde yükle
            api_key = os.environ.get("GOOGLE_API_KEY")
            if not api_key:
                await ctx.send("Hata: API anahtarı ayarlanmamış!")
                return
            
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            response = model.generate_content(soru)
            await ctx.send(response.text)
        except Exception as e:
            await ctx.send(f"Hata detayı: {str(e)}")

@bot.command()
async def valdo(ctx): await ctx.send("YARRAMM VALDO BU KIM AMK")
@bot.command()
async def gonu(ctx): await ctx.send("2 GUNDE 48 CK ATAN ADAM")
@bot.command()
async def eternal(ctx): await ctx.send("FURKANIN NAMIDEGER BABASI")
@bot.command()
async def klowinc(ctx): await ctx.send("BU ADAMIN TASSAKLARINA BETON YETMEZ")
@bot.command()
async def doruk(ctx): await ctx.send("ARİEL BABAAAA")

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.name} banlandı!')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, miktar: int):
    await ctx.channel.purge(limit=miktar + 1)
    await ctx.send(f'{miktar} mesaj silindi.', delete_after=3)

@bot.command()
@commands.has_permissions(administrator=True)
async def spam(ctx):
    global spam_aktif
    if spam_aktif: return
    spam_aktif = True
    await ctx.send("Spam başlatıldı!")
    while spam_aktif:
        await ctx.send("KLOWINC BİR UGRADI! @everyone")
        await asyncio.sleep(0.5)

@bot.command()
@commands.has_permissions(administrator=True)
async def dur(ctx):
    global spam_aktif
    spam_aktif = False
    await ctx.send("Spam durduruldu.")

@bot.command()
async def yardım(ctx):
    await ctx.send("Komutlar: !valdo, !gonu, !eternal, !klowinc, !doruk, !sor [soru], !ban, !clear, !spam, !dur")

# --- Başlatma ---
if __name__ == "__main__":
    init_db()
    Thread(target=run_web).start()
    token = os.environ.get('DISCORD_TOKEN')
    if token: bot.run(token)