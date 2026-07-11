import discord
from discord.ext import commands
import asyncio
import os
import sqlite3
from datetime import timedelta
from flask import Flask
from threading import Thread

# --- Flask Web Sunucusu (7/24 Aktiflik) ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot aktif!"
def run_web(): app.run(host='0.0.0.0', port=8080)

# --- AYARLAR ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Global Durumlar
spam_aktif = False
silme_aktif = False

# --- VERİTABANI ---
def init_db():
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS uyari (user_id INTEGER, sayi INTEGER)')
    conn.commit()
    conn.close()

# --- ETKİNLİKLER ---
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!yardım"))
    print(f'Bot hazır: {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Yetkin yetmiyor, otur ağla :::")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❓ Böyle bir komut yok.")

# --- EĞLENCE KOMUTLARI ---
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
async def furkan(ctx, text=None):
    if text == 'video':
        if os.path.exists('furkan.mp4'): await ctx.send(file=discord.File('furkan.mp4'))
        else: await ctx.send("Hata: furkan.mp4 bulunamadı!")
    else: await ctx.send("AMCIK FURKO")

@bot.command()
async def atam(ctx):
    if os.path.exists('ataturk.jpg'): await ctx.send(file=discord.File('ataturk.jpg'))
    else: await ctx.send("Hata: Dosya bulunamadı!")

# --- MODERASYON KOMUTLARI ---
@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.name} banlandı!')

@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.name} atıldı.')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, miktar: int):
    await ctx.channel.purge(limit=miktar + 1)
    await ctx.send(f'{miktar} mesaj silindi.', delete_after=3)

# --- SPAM VE SİLME (Yönetici Yetkisi ile) ---
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
@commands.has_permissions(administrator=True)
async def sil(ctx):
    global silme_aktif
    silme_aktif = True
    await ctx.send("Kanallar siliniyor...")
    for kanal in ctx.guild.channels:
        if not silme_aktif: break
        try: await kanal.delete()
        except: continue

# --- YARDIM ---
@bot.command()
async def yardım(ctx):
    await ctx.send("Mevcut Komutlar: !valdo, !gonu, !eternal, !klowinc, !doruk, !furkan, !atam, !ban, !kick, !clear, !spam, !dur, !sil")

# --- BAŞLATMA ---
if __name__ == "__main__":
    init_db()
    Thread(target=run_web).start()
    token = os.environ.get('DISCORD_TOKEN')
    if token: bot.run(token)