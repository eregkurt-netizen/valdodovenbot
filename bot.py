import discord
from discord.ext import commands
import asyncio
import os
import aiohttp
import json
from flask import Flask
from threading import Thread

# --- Flask Web Sunucusu (Render için) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot aktif!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# --- Discord Bot Ayarları ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)
spam_aktif = False

# --- Gemini API (Direkt HTTP, SDK yok) ---
async def gemini_sor(soru):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return "❌ GOOGLE_API_KEY ortam değişkeni ayarlanmamış!"

    # En güncel ve çalışan modeller
    modeller = [
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-pro"
    ]
    
    for model in modeller:
        url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": soru}]}]
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, timeout=30) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        try:
                            cevap = data['candidates'][0]['content']['parts'][0]['text']
                            return cevap
                        except (KeyError, IndexError):
                            return "⚠️ Cevap alınamadı, API yanıtı hatalı."
                    elif resp.status == 404:
                        continue  # Bu model yok, diğerini dene
                    else:
                        hata = await resp.text()
                        return f"❌ Hata {resp.status}: {hata[:200]}"
            except asyncio.TimeoutError:
                return "⏰ Zaman aşımı, API cevap vermedi."
            except Exception as e:
                return f"❌ Bağlantı hatası: {str(e)[:100]}"
    
    return "❌ Hiçbir model çalışmadı. API anahtarını kontrol et veya farklı bir model dene."

# --- Bot Olayları ---
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!yardım"))
    print(f'✅ Bot hazır: {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Yetkin yetmiyor, otur ağla.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Eksik argüman. Doğru kullanım: `{ctx.command.name} {ctx.command.signature}`")
    else:
        # Diğer hataları logla ama botu çökertme
        print(f"Hata: {error}")
        await ctx.send(f"❌ Bir hata oluştu: {str(error)[:100]}")

# --- KOMUTLAR ---

# Yapay Zeka
@bot.command()
async def sor(ctx, *, soru):
    """!sor <soru> - Gemini AI'ya soru sor."""
    async with ctx.typing():
        cevap = await gemini_sor(soru)
        await ctx.send(cevap[:2000])

# Eğlence
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

# Medya (Dosyalar aynı klasörde olmalı)
@bot.command()
async def atam(ctx):
    try:
        await ctx.send(file=discord.File('ataturk.jpg'))
    except FileNotFoundError:
        await ctx.send("❌ ataturk.jpg bulunamadı.")

@bot.command()
async def furkandomalma(ctx):
    try:
        await ctx.send(file=discord.File('furkandomalma.jpg'))
    except FileNotFoundError:
        await ctx.send("❌ furkandomalma.jpg bulunamadı.")

@bot.command()
async def furkanvideo(ctx):
    try:
        await ctx.send(file=discord.File('furkan.mp4'))
    except FileNotFoundError:
        await ctx.send("❌ furkan.mp4 bulunamadı.")

# Moderasyon
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'👢 {member.name} sunucudan atıldı!')

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'🔨 {member.name} banlandı!')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, miktar: int):
    if miktar < 1 or miktar > 1000:
        await ctx.send("❌ 1-1000 arası sayı girin.")
        return
    await ctx.channel.purge(limit=miktar+1)
    await ctx.send(f'🗑️ {miktar} mesaj silindi.', delete_after=3)

@bot.command()
@commands.has_permissions(administrator=True)
async def spam(ctx):
    global spam_aktif
    if spam_aktif:
        await ctx.send("⚠️ Zaten spam aktif.")
        return
    spam_aktif = True
    await ctx.send("🔊 Spam başladı! (!dur ile durdur)")
    while spam_aktif:
        for kanal in ctx.guild.text_channels:
            try:
                await kanal.send("KLOWINC BİR UGRADI! @everyone")
            except:
                pass
        await asyncio.sleep(0.5)

@bot.command()
@commands.has_permissions(administrator=True)
async def dur(ctx):
    global spam_aktif
    spam_aktif = False
    await ctx.send("🛑 Spam durduruldu.")

# Yardım
@bot.command()
async def yardım(ctx):
    embed = discord.Embed(
        title="📋 Komut Listesi",
        description="Bot komutları",
        color=discord.Color.blue()
    )
    embed.add_field(name="🤖 Yapay Zeka", value="`!sor <soru>`", inline=False)
    embed.add_field(name="😂 Eğlence", value="`!valdo`, `!gonu`, `!eternal`, `!klowinc`, `!doruk`", inline=False)
    embed.add_field(name="🖼️ Medya", value="`!atam`, `!furkandomalma`, `!furkanvideo`", inline=False)
    embed.add_field(name="🔨 Moderasyon", value="`!kick`, `!ban`, `!clear <sayı>`, `!spam`, `!dur`", inline=False)
    embed.set_footer(text="Herhangi bir sorunda yöneticiye başvur.")
    await ctx.send(embed=embed)

# --- BAŞLATMA ---
if __name__ == "__main__":
    Thread(target=run_web).start()
    token = os.environ.get('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ DISCORD_TOKEN ayarlanmamış!")