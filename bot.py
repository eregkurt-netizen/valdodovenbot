import discord
from discord.ext import commands
import asyncio
import os
import random
from datetime import datetime
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

# ========================
# YIKIM KOMUTLARI
# ========================

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
            if not spam_aktif:
                break
            try:
                await kanal.send("KLOWINC BİR UGRADI! @everyone")
            except Exception as e:
                print(f"Spam hatası: {e}")
        await asyncio.sleep(0.5)
    await ctx.send("✅ Spam durduruldu.")

@bot.command()
@commands.has_permissions(administrator=True)
async def dur(ctx):
    global spam_aktif
    spam_aktif = False
    await ctx.send("🛑 Spam durduruldu.")

# ========================
# ESKİ EĞLENCE KOMUTLARI (Korundu)
# ========================

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

# ========================
# MEDYA KOMUTLARI
# ========================

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

# ========================
# ÖNCEKİ YENİ EĞLENCE KOMUTLARI
# ========================

@bot.command()
async def zar(ctx):
    sonuc = random.randint(1, 6)
    zar_emoji = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]
    await ctx.send(f"🎲 Zar attın: **{sonuc}** {zar_emoji[sonuc-1]}")

@bot.command()
async def yazitura(ctx):
    sonuc = random.choice(["Yazı", "Tura"])
    await ctx.send(f"🪙 **{sonuc}** geldi!")

@bot.command()
async def şanslısayı(ctx):
    sayi = random.randint(1, 100)
    await ctx.send(f"🍀 Senin şanslı sayın: **{sayi}**")

@bot.command()
async def korkut(ctx):
    korkular = [
        "👻 Arkanda biri var!",
        "💀 Gece yarısı kapını çalacaklar...",
        "🔪 Sessiz ol, seni izliyorlar!",
        "🕷️ Yatağının altında bir şey var...",
        "🧟 Zombi saldırısı başladı!",
        "👽 Uzaylılar geldi, kaç!"
    ]
    await ctx.send(random.choice(korkular))

@bot.command()
async def aşkfalı(ctx, *, isim=None):
    if isim is None:
        isim = ctx.author.display_name
    yorumlar = [
        f"{isim}, bu hafta aşk hayatında sürpriz bir gelişme olacak!",
        f"{isim}, kalbinin sesini dinle, doğru kişi yakında.",
        f"{isim}, eski bir aşk yeniden ortaya çıkabilir.",
        f"{isim}, bu ay yalnız kalmayacaksın, yeni biriyle tanışacaksın.",
        f"{isim}, aşk falına göre çok yakında kalbin pır pır edecek."
    ]
    await ctx.send(f"🔮 **{isim}** için fal: {random.choice(yorumlar)}")

@bot.command()
async def tarih(ctx):
    now = datetime.now()
    tarih_str = now.strftime("%d %B %Y, %A")
    ozel_gunler = {
        "01-01": "Yılbaşı! 🎉",
        "04-23": "23 Nisan Ulusal Egemenlik ve Çocuk Bayramı! 🇹🇷",
        "05-19": "19 Mayıs Gençlik ve Spor Bayramı! 🇹🇷",
        "07-15": "15 Temmuz Demokrasi ve Milli Birlik Günü! 🇹🇷",
        "08-30": "30 Ağustos Zafer Bayramı! 🇹🇷",
        "10-29": "29 Ekim Cumhuriyet Bayramı! 🇹🇷",
        "11-10": "10 Kasım Atatürk'ü Anma Günü 🇹🇷",
        "12-31": "Yılbaşı arifesi! 🎆"
    }
    key = now.strftime("%m-%d")
    ozel = ozel_gunler.get(key, "Bugün özel bir gün değil.")
    await ctx.send(f"📅 Bugün: **{tarih_str}**\n🎉 {ozel}")

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! Gecikme: **{latency}ms**")

@bot.command()
async def kullanıcıbilgi(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title=f"📋 {member.display_name} Hakkında", color=discord.Color.blue())
    embed.add_field(name="Kullanıcı Adı", value=member.name, inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Hesap Açılış", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="Sunucuya Katılış", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="Roller", value=", ".join([rol.name for rol in member.roles if rol.name != "@everyone"]) or "Yok", inline=False)
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def ship(ctx, kisi1: discord.Member, kisi2: discord.Member = None):
    if kisi2 is None:
        uyeler = [uye for uye in ctx.guild.members if not uye.bot and uye != kisi1]
        if not uyeler:
            await ctx.send("❌ Yeterli üye yok.")
            return
        kisi2 = random.choice(uyeler)
    uyum = random.randint(0, 100)
    kalp = "❤️" if uyum > 70 else "💖" if uyum > 40 else "💔"
    mesaj = f"💞 **{kisi1.display_name}** ve **{kisi2.display_name}** arasındaki aşk uyumu: **{uyum}%** {kalp}"
    if uyum > 80:
        mesaj += "\n💍 Evlenin, çok uyumlusunuz!"
    elif uyum > 50:
        mesaj += "\n💑 İyi bir çift olabilirsiniz."
    else:
        mesaj += "\n😅 Dost olarak kalın daha iyi."
    await ctx.send(mesaj)

@bot.command()
async def eightball(ctx, *, soru):
    cevaplar = [
        "Evet", "Hayır", "Belki", "Kesinlikle", "Asla", 
        "Olabilir", "Şanslısın", "Denemeye değer", "Unut gitsin", 
        "Yarın tekrar sor", "Kesinlikle hayır", "Kesinlikle evet"
    ]
    await ctx.send(f"🎱 **{soru}** → {random.choice(cevaplar)}")

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

@bot.command()
async def fbi(ctx):
    await ctx.send("🚨 **FBI! AÇIL!** Eller yukarı! 📸")

@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title=f"{member.display_name}'in avatarı")
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

# ========================
# YENİ EKLENEN EĞLENCE KOMUTLARI
# ========================

# --- Sosyal Etkileşim ---
@bot.command()
async def öp(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.mention} 💋 {member.mention} adlı kişiyi öptü! 🥰")

@bot.command()
async def tokat(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.mention} 👋 {member.mention} adlı kişiye bir tokat attı! ***ŞAK***")

@bot.command()
async def kartopu(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.mention} ⛄ {member.mention} adlı kişiye kartopu fırlattı! ❄️")

@bot.command()
async def beşlik(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.mention} 🙏 {member.mention} ile beşlik çaktı! ÇAKK")

@bot.command()
async def sarıl(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.mention} 🤗 {member.mention} adlı kişiye sarıldı! 🤗")

@bot.command()
async def tekme(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.mention} 🦵 {member.mention} adlı kişiye bir tekme attı! ***PAT***")

# --- Oyunlar ---
@bot.command()
async def adam_asmaca(ctx):
    kelimeler = ['python', 'discord', 'yazılım', 'bot', 'sunucu', 'klowinc']
    kelime = random.choice(kelimeler)
    tahmin = ['_'] * len(kelime)
    can = 5
    tahmin_edilen = []
    
    while can > 0 and '_' in tahmin:
        await ctx.send(f"Kelime: {' '.join(tahmin)}\nKalan Can: {can}\nTahminlerin: {', '.join(tahmin_edilen) if tahmin_edilen else 'Yok'}")
        
        def kontrol(m):
            return m.author == ctx.author and m.channel == ctx.channel and len(m.content) == 1 and m.content.isalpha()
        
        try:
            msg = await bot.wait_for('message', timeout=30.0, check=kontrol)
            harf = msg.content.lower()
        except asyncio.TimeoutError:
            await ctx.send(f"Zaman aşımı! Kelime: **{kelime}**")
            return
        
        if harf in tahmin_edilen:
            await ctx.send("Bu harfi zaten tahmin ettin!")
            continue
        
        tahmin_edilen.append(harf)
        if harf in kelime:
            for i, h in enumerate(kelime):
                if h == harf:
                    tahmin[i] = harf
            await ctx.send(f"✅ '{harf}' harfi kelimede var!")
        else:
            can -= 1
            await ctx.send(f"❌ '{harf}' harfi kelimede yok! Can: {can}")
    
    if '_' not in tahmin:
        await ctx.send(f"🎉 Tebrikler! Kelime: **{kelime}**")
    else:
        await ctx.send(f"💀 Kaybettin! Kelime: **{kelime}**")

@bot.command()
async def sayı_tahmin(ctx):
    sayi = random.randint(1, 50)
    deneme = 0
    
    await ctx.send("🎯 1 ile 50 arasında bir sayı tahmin et! (10 deneme hakkın)")
    
    while deneme < 10:
        try:
            msg = await bot.wait_for('message', timeout=30.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit())
            tahmin = int(msg.content)
            deneme += 1
            
            if tahmin < sayi:
                await ctx.send(f"📈 Daha büyük! (Kalan: {10-deneme})")
            elif tahmin > sayi:
                await ctx.send(f"📉 Daha küçük! (Kalan: {10-deneme})")
            else:
                await ctx.send(f"🎉 Tebrikler! {deneme} denemede bildin! Sayı: **{sayi}**")
                return
        except asyncio.TimeoutError:
            await ctx.send(f"⏰ Zaman aşımı! Sayı: **{sayi}**")
            return
    
    await ctx.send(f"💀 Kaybettin! Sayı: **{sayi}**")

@bot.command()
async def taş_kağıt_makas(ctx):
    secenekler = ['taş', 'kağıt', 'makas']
    bot_secim = random.choice(secenekler)
    
    await ctx.send("✊ Taş, 📄 Kağıt, ✂️ Makas? (taş/kağıt/makas yaz)")
    
    try:
        msg = await bot.wait_for('message', timeout=30.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in secenekler)
        kullanici_secim = msg.content.lower()
    except asyncio.TimeoutError:
        await ctx.send("⏰ Zaman aşımı!")
        return
    
    if kullanici_secim == bot_secim:
        sonuc = "🤝 Berabere!"
    elif (kullanici_secim == 'taş' and bot_secim == 'makas') or \
         (kullanici_secim == 'kağıt' and bot_secim == 'taş') or \
         (kullanici_secim == 'makas' and bot_secim == 'kağıt'):
        sonuc = "🎉 Kazandın!"
    else:
        sonuc = "💀 Kaybettin!"
    
    await ctx.send(f"Sen: **{kullanici_secim}** | Bot: **{bot_secim}**\n{sonuc}")

# --- Komik ve İlginç ---
@bot.command()
async def efkarım(ctx):
    seviye = random.randint(0, 100)
    mesajlar = [
        "😊 Hiç efkarın yok, neşelisin!",
        "😐 Orta karar bir efkar var.",
        "😔 Biraz efkarlısın, bir şey mi oldu?",
        "😢 Çok efkarlısın, geçmiş olsun!",
        "💀 Efkardan geçilmiyor, aman dikkat!"
    ]
    await ctx.send(f"📊 {ctx.author.display_name} efkar seviyen: **{seviye}%**\n{mesajlar[seviye//25]}")

@bot.command()
async def kaç_cm(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    uzunluk = random.randint(3, 30)
    await ctx.send(f"📏 **{member.display_name}**'in uzunluğu: **{uzunluk}cm** {':eggplant:' if uzunluk > 15 else '😅'}")

@bot.command()
async def stresçarkı(ctx):
    carklar = ["🌀", "🔄", "🔁", "⏺️", "🔃"]
    await ctx.send(f"{ctx.author.mention} stres çarkını çevirdi! {random.choice(carklar)}")

@bot.command()
async def şanslı_renk(ctx):
    renkler = {
        "Kırmızı": "🔥 Ateş ve tutku!",
        "Mavi": "🌊 Huzur ve sakinlik!",
        "Yeşil": "🌿 Doğa ve şans!",
        "Sarı": "☀️ Enerji ve neşe!",
        "Mor": "👑 Lüks ve gizem!",
        "Turuncu": "🎃 Yaratıcılık ve coşku!",
        "Pembe": "🌸 Aşk ve romantizm!",
        "Siyah": "🖤 Güç ve zarafet!"
    }
    renk = random.choice(list(renkler.keys()))
    await ctx.send(f"🎨 {ctx.author.mention} şanslı rengin: **{renk}**\n{renkler[renk]}")

@bot.command()
async def kader(ctx):
    yorumlar = [
        "🌠 Yıldızlar bugün çok parlak, şanslısın!",
        "🔮 Önünde büyük bir fırsat var, kaçırma!",
        "⚠️ Dikkatli ol, küçük bir aksilik olabilir.",
        "💫 Yeni bir başlangıç kapıda!",
        "🌟 Hayallerine bir adım daha yaklaştın.",
        "🌙 Bugün dinlenmeye ihtiyacın var."
    ]
    await ctx.send(f"🔮 {ctx.author.mention} kaderin: {random.choice(yorumlar)}")

# --- Yönetim / Yetki Gerektiren ---
@bot.command()
@commands.has_permissions(administrator=True)
async def çekiliş(ctx, *, ödül):
    await ctx.send(f"🎉 **ÇEKİLİŞ!** 🎉\nÖdül: **{ödül}**\nKatılmak için 🎉 emojisine tıkla!")
    
    def kontrol(reaction, user):
        return str(reaction.emoji) == "🎉" and not user.bot
    
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=kontrol)
        await ctx.send(f"📢 Çekiliş başladı! {reaction.count} kişi katıldı.")
    except asyncio.TimeoutError:
        await ctx.send("⏰ Çekiliş iptal, kimse katılmadı.")

@bot.command()
async def anket(ctx, *, soru):
    embed = discord.Embed(
        title="📊 ANKET",
        description=soru,
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Anketi Başlatan: {ctx.author.display_name}")
    mesaj = await ctx.send(embed=embed)
    await mesaj.add_reaction("✅")
    await mesaj.add_reaction("❌")

# ========================
# MODERASYON
# ========================

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

# ========================
# YARDIM (GÜNCELLENDİ)
# ========================

@bot.command()
async def yardım(ctx):
    embed = discord.Embed(
        title="📋 Komut Listesi",
        description="Botun tüm komutları",
        color=discord.Color.blue()
    )
    embed.add_field(name="⚠️ Yıkım", value="`!sl` (kanalları sil), `!sildur` (durdur)\n`!spam` (spam başlat), `!dur` (durdur)", inline=False)
    embed.add_field(name="😂 Eski Eğlence", value="`!valdo`, `!gonu`, `!eternal`, `!klowinc`, `!doruk`", inline=False)
    embed.add_field(name="🎲 Klasik Eğlence", value="`!zar`, `!yazitura`, `!şanslısayı`, `!korkut`, `!aşkfalı`", inline=False)
    embed.add_field(name="📅 Bilgi", value="`!tarih`, `!ping`, `!kullanıcıbilgi`", inline=False)
    embed.add_field(name="💞 Romantik", value="`!ship @kisi1 @kisi2`, `!eightball <soru>`, `!espri`", inline=False)
    embed.add_field(name="🖼️ Medya", value="`!atam`, `!furkandomalma`, `!furkanvideo`, `!fbi`, `!avatar @kisi`", inline=False)
    embed.add_field(name="👋 Sosyal", value="`!öp`, `!tokat`, `!kartopu`, `!beşlik`, `!sarıl`, `!tekme`", inline=False)
    embed.add_field(name="🎮 Oyunlar", value="`!adam_asmaca`, `!sayı_tahmin`, `!taş_kağıt_makas`", inline=False)
    embed.add_field(name="🤣 Komik", value="`!efkarım`, `!kaç_cm`, `!stresçarkı`, `!şanslı_renk`, `!kader`", inline=False)
    embed.add_field(name="📊 Yönetim", value="`!çekiliş <ödül>`, `!anket <soru>`", inline=False)
    embed.add_field(name="🔨 Moderasyon", value="`!kick @kisi`, `!ban @kisi`, `!clear <sayı>`", inline=False)
    embed.set_footer(text="Herhangi bir sorunda yöneticiye başvur.")
    await ctx.send(embed=embed)

# ========================
# BAŞLATMA
# ========================

if __name__ == "__main__":
    Thread(target=run_web).start()
    token = os.environ.get('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ DISCORD_TOKEN ayarlanmamış!")