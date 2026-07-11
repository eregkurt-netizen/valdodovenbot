import discord
from discord.ext import commands
import asyncio
import os
import sqlite3
import aiohttp
from flask import Flask
from threading import Thread

# --- Web Sunucusu (Render için) ---
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot aktif!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# --- Bot Ayarları ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
spam_aktif = False

# --- Veritabanı (ileride kullanılmak üzere) ---
def init_db():
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS uyari (user_id INTEGER, sayi INTEGER)')
    conn.commit()
    conn.close()

init_db()

# --- AI Fonksiyonu (HTTP isteği ile, SDK'sız) ---
async def gemini_sor(soru):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "❌ GOOGLE_API_KEY ortam değişkeni ayarlanmamış!"

    # Önce 1.5-flash dene, olmazsa gemini-pro dene
    modeller = ["gemini-1.5-flash", "gemini-pro"]
    for model in modeller:
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": soru}]}]}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    try:
                        cevap = data['candidates'][0]['content']['parts'][0]['text']
                        return cevap
                    except (KeyError, IndexError):
                        return "⚠️ Cevap alınamadı, API yanıtı beklenen formatta değil."
                elif resp.status == 404:
                    # Bu model bulunamadı, diğerini dene
                    continue
                else:
                    hata = await resp.text()
                    return f"❌ API Hatası ({resp.status}): {hata}"

    return "❌ Hiçbir model çalışmadı. API anahtarını veya model isimlerini kontrol et."

# --- Olaylar ---
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!yardım"))
    print(f'Bot hazır: {bot.user}')

# --- AI Sohbet Komutu ---
@bot.command()
async def sor(ctx, *, soru):
    """Gemini yapay zekaya soru sor."""
    async with ctx.typing():
        cevap = await gemini_sor(soru)
        # Discord mesaj limiti 2000 karakter, onu aşmamak için kırp
        if len(cevap) > 2000:
            cevap = cevap[:1997] + "..."
        await ctx.send(cevap)

# --- Eğlence Komutları (Senin özel) ---
@bot.command()
async def valdo(ctx):
    await ctx.send("YARRAMM VALDO BU KIM AMK")

@bot.command()
async def gonu(ctx):
    await ctx.send("2 GUNDE 48 CK ATAN ADAM")

@bot.command()
async def eternal(ctx):
    await ctx.send("FURKANIN NAMIDEGER BABASI")

@bot.command()
async def klowinc(ctx):
    await ctx.send("BU ADAMIN TASSAKLARINA BETON YETMEZ")

@bot.command()
async def doruk(ctx):
    await ctx.send("ARİEL BABAAAA")

# --- Medya Komutları (Dosyaların olduğundan emin ol) ---
@bot.command()
async def atam(ctx):
    try:
        await ctx.send(file=discord.File('ataturk.jpg'))
    except FileNotFoundError:
        await ctx.send("❌ ataturk.jpg dosyası bulunamadı.")

@bot.command()
async def furkandomalma(ctx):
    try:
        await ctx.send(file=discord.File('furkandomalma.jpg'))
    except FileNotFoundError:
        await ctx.send("❌ furkandomalma.jpg dosyası bulunamadı.")

@bot.command()
async def furkanvideo(ctx):
    try:
        await ctx.send(file=discord.File('furkan.mp4'))
    except FileNotFoundError:
        await ctx.send("❌ furkan.mp4 dosyası bulunamadı.")

# --- Moderasyon Komutları ---
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.name} sunucudan siktir edildi!')

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.name} kalıcı olarak banlandı!')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, miktar: int):
    await ctx.channel.purge(limit=miktar + 1)
    await ctx.send(f'{miktar} mesaj silindi.', delete_after=3)

@bot.command()
@commands.has_permissions(administrator=True)
async def spam(ctx):
    global spam_aktif
    if spam_aktif:
        await ctx.send("Zaten spam aktif!")
        return
    spam_aktif = True
    await ctx.send("Spam başlatıldı! (Durdurmak için !dur)")
    while spam_aktif:
        await ctx.send("KLOWINC BİR UGRADI! @everyone")
        await asyncio.sleep(0.5)

@bot.command()
@commands.has_permissions(administrator=True)
async def dur(ctx):
    global spam_aktif
    spam_aktif = False
    await ctx.send("Spam durduruldu.")

# --- Yardım Komutu (Basit) ---
@bot.command()
async def yardım(ctx):
    yardim_mesaji = (
        "**📌 Kullanılabilir Komutlar:**\n"
        "`!sor <soru>` - Gemini AI'ya soru sor\n"
        "`!valdo`, `!gonu`, `!eternal`, `!klowinc`, `!doruk` - Eğlence\n"
        "`!atam`, `!furkandomalma`, `!furkanvideo` - Medya göster\n"
        "`!kick <@kullanıcı> [sebep]` - Üye at (kick yetkisi gerekli)\n"
        "`!ban <@kullanıcı> [sebep]` - Üye banla (admin)\n"
        "`!clear <miktar>` - Mesaj sil (mesaj yönetimi yetkisi)\n"
        "`!spam` - Spam başlat (admin)\n"
        "`!dur` - Spam'ı durdur (admin)\n"
        "`!yardım` - Bu mesajı gösterir"
    )
    await ctx.send(yardim_mesaji)

# --- Başlatma ---
if __name__ == "__main__":
    # Web sunucusunu ayrı bir thread'de başlat
    Thread(target=run_web).start()
    token = os.environ.get('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("DISCORD_TOKEN ortam değişkeni ayarlanmamış!")