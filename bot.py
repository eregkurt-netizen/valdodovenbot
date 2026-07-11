import discord
from discord.ext import commands
import asyncio
import os
from datetime import timedelta
from flask import Flask
from threading import Thread

# --- Flask Web Sunucusu (7/24 Aktiflik İçin) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot aktif!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# --- AYARLAR ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

spam_aktif = False
silme_aktif = False
VIDEO_DOSYA_ADI = 'furkan.mp4'

@bot.event
async def on_ready():
    print(f'Bot hazır: {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Yetkin yetmiyor, otur ağla :::")
    else:
        raise error

# --- KOMUTLAR (Aynı) ---
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

@bot.command(name='furkan')
async def furkan_komutu(ctx, text=None):
    if text and text.lower() == 'video':
        if os.path.exists(VIDEO_DOSYA_ADI):
            await ctx.send(file=discord.File(VIDEO_DOSYA_ADI))
        else: await ctx.send("Hata: furkan.mp4 bulunamadı!")
    else: await ctx.send("AMCIK FURKO")

@bot.command()
async def atam(ctx):
    if os.path.exists('ataturk.jpg'): await ctx.send(file=discord.File('ataturk.jpg'))
    else: await ctx.send("Hata: ataturk.jpg bulunamadı!")

@bot.command()
async def furkandomalma(ctx):
    if os.path.exists('furkandomalma.jpg'): await ctx.send(file=discord.File('furkandomalma.jpg'))
    else: await ctx.send("Hata: furkandomalma.jpg bulunamadı!")

# --- YÖNETİCİ KOMUTLARI ---
@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.name} sunucudan banlandı!')

@bot.command()
@commands.has_permissions(administrator=True)
async def sustur(ctx, member: discord.Member, dakika: int):
    duration = timedelta(minutes=dakika)
    await member.timeout(duration, reason="Yönetici susturdu")
    await ctx.send(f'{member.name} {dakika} dakikalığına susturuldu.')

@bot.command()
@commands.has_permissions(administrator=True)
async def ac(ctx, member: discord.Member):
    await member.timeout(None, reason="Susturma kaldırıldı")
    await ctx.send(f'{member.name} susturması kaldırıldı.')

@bot.command()
@commands.has_permissions(administrator=True)
async def spam(ctx):
    global spam_aktif
    if spam_aktif: return
    spam_aktif = True
    await ctx.send("Spam başlatıldı!")
    while spam_aktif:
        tasks = [kanal.send("KLOWINC BİR UGRADI! @everyone") for kanal in ctx.guild.text_channels]
        await asyncio.gather(*tasks, return_exceptions=True)
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
    await ctx.send("Kanallar 5 saniye arayla siliniyor...")
    for kanal in ctx.guild.channels:
        if not silme_aktif: break
        try:
            await kanal.delete()
            await asyncio.sleep(5)
        except Exception as e: print(f"Hata: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def dur_sil(ctx):
    global silme_aktif
    silme_aktif = False
    await ctx.send("Kanal silme durduruldu.")

# --- BAŞLATMA ---
if __name__ == "__main__":
    Thread(target=run_web).start() # Web sunucusunu başlat
    token = os.environ.get('DISCORD_TOKEN')
    if token: bot.run(token)