import discord
from discord.ext import commands
import asyncio
import os # Dosya kontrolü için gerekli

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

spam_aktif = False
silme_aktif = False

# Bilgisayarındaki 'furkan.mp4' dosyasının adı
VIDEO_DOSYA_ADI = 'furkan.mp4'

@bot.event
async def on_ready():
    print(f'Bot hazır: {bot.user}')

# --- MESAJ KOMUTLARI ---
@bot.command()
async def valdo(ctx):
    await ctx.send("YARRAMM VALDO BU KIM AMK")

@bot.command()
async def eternal(ctx):
    await ctx.send("FURKANIN NAMIDEGER BABASI") 

@bot.command()
async def klowinc(ctx):
    await ctx.send("BU ADAMIN TASSAKLARINA BETON YETMEZ") 

@bot.command()  
async def gonu(ctx):
    await ctx.send("BU ADAM 2 GUNDE 48 CK ATTI UZAK DUR RİSKLİ")

@bot.command()
async def doruk(ctx):
    await ctx.send("ARİEL BABAAAA")

# --- FURKAN KOMUTU (GÜNCELLENDİ) ---
@bot.command(name='furkan') # Komut ismini 'furkan' yapıyoruz
async def furkan_komutu(ctx, text=None): # Artık argüman alabilir
    # Eğer '!furkavideo' yazıldıysa video at
    if text and text.lower() == 'video':
        await ctx.send("Video yükleniyor...")
        if os.path.exists(VIDEO_DOSYA_ADI):
            try:
                await ctx.send(file=discord.File(VIDEO_DOSYA_ADI))
            except Exception as e:
                await ctx.send(f"Hata: Video gönderilemedi! ({e})")
        else:
            await ctx.send(f"Hata: '{VIDEO_DOSYA_ADI}' dosyası klasörde bulunamadı!")
    else:
        # Eğer sadece '!furkan' yazıldıysa eski mesajı at
        await ctx.send("AMCIK FURKO")

@bot.command()
async def atam(ctx):
    # Bilgisayarındaki 'ataturk.jpg' dosyasını yükler
   import discord
from discord.ext import commands
import asyncio
import os
from datetime import timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.members = True # Üyeleri banlamak/susturmak için zorunludur

bot = commands.Bot(command_prefix='!', intents=intents)

# Durum değişkenleri
spam_aktif = False
silme_aktif = False
VIDEO_DOSYA_ADI = 'furkan.mp4'

@bot.event
async def on_ready():
    print(f'Bot hazır: {bot.user}')

# --- HERKESİN KULLANABİLECEĞİ KOMUTLAR ---

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

@bot.command(name='furkan')
async def furkan_komutu(ctx, text=None):
    if text and text.lower() == 'video':
        if os.path.exists(VIDEO_DOSYA_ADI):
            await ctx.send(file=discord.File(VIDEO_DOSYA_ADI))
        else:
            await ctx.send("Hata: furkan.mp4 dosyası bulunamadı!")
    else:
        await ctx.send("AMCIK FURKO")

@bot.command()
async def atam(ctx):
    if os.path.exists('ataturk.jpg'):
        await ctx.send(file=discord.File('ataturk.jpg'))
    else:
        await ctx.send("Hata: ataturk.jpg dosyası bulunamadı!")

# --- YÖNETİCİ KOMUTLARI (BAN, SUSTUR, SPAM, SİL) ---

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
    await ctx.send("Kanallar 5 saniye arayla silinmeye başlanıyor...")
    for kanal in ctx.guild.channels:
        if not silme_aktif: break
        try:
            await kanal.delete()
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Kanal silinemedi: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def dur_sil(ctx):
    global silme_aktif
    silme_aktif = False
    await ctx.send("Kanal silme işlemi durduruldu.")

bot.run('')