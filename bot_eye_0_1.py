import discord
from discord.ext import commands
from random import randint 
from discord.utils import get
from discord import FFmpegPCMAudio
#from youtube_dl import YoutubeDL
import youtube_dl
import urllib.parse,urllib.request,re
from youtube_search import YoutubeSearch
import time 
from time import ctime


youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}	
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

result_check=  ["เค้าอยู่นี่","ว่างายย","มีอะไรหรอ ?","เรียกเค้าทำไมหรอ ?","มีอะไรให้ช่วยหรอ ? ","มีรายยยยยย"]
result_hungry = [" ป่ะๆ หาไรกินกันนนนน","หาอะไรกินก่อนก็ด้ายยยยย","ลองออกไปหาอะไรกินสิ ^^","หิวต่อไป ไม่ยอมหาไรกินเองอ่ะ -*- ","งั้นหาไรกินกันเถอะ","ไปหาไรกินเลยยย"]
result_bored = ["ลองหาไรทำดูมั้ยล่ะ ^^","ลองดูเมะสิ น่าจะช่วยได้นะ","แนะนำให้หาเกมเล่นค่าา","หาเพื่อนเล่นเกมสิ","ดู Netflix สิ ><","ดู Youtube"," Vtuber"]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def Serch_url(text):
	serach_results = YoutubeSearch(text, max_results=1).to_dict()
	data = str(serach_results)
	data = data.split(", ")
	data_result = str(data[9])
	data_result = data_result.split("/")
	data_return = str(data_result[1])
	data_return = data_return.split("'")
	data_return = str(data_return[0])
	output_result = "https://www.youtube.com/"+data_return
	print(output_result)
	return output_result

def randomResult(num):
	data_random = randint(0,num)
	return data_random

@bot.command()
async def check(ctx):
	num = randomResult(5)
	await ctx.channel.send((result_check[num]))

@bot.command()
async def p(ctx, music_name):
	channel = ctx.author.voice.channel
	voice_client = get(bot.voice_clients,guild = ctx.guild)

	if voice_client == None :
		ctx.channel.send("เค้ามาแล้ววว")
		await channel.connect()
		voice_client = get(bot.voice_clients, guild = ctx.guild)

	VOICE_OPTOINS = {
		'format': 'bestaudio/best',
    	'restrictfilenames': True,
    	'noplaylist': True,
    	'nocheckcertificate': True,
    	'ignoreerrors': False,
    	'logtostderr': False,
    	'quiet': True,
    	'no_warnings': True,
    	'default_search': 'auto',
    	'source_address': '0.0.0.0'}
	FFMPEG_OPTIONS = {
		'options': '-vn'
		}

	if not voice_client.is_playing():
		url = music_name
		with YoutubeDL(VOICE_OPTOINS) as ydl :
			info = ydl.extract_info(url, download=False)
		URL = info['formats'][0]['url']
		voice_client.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS))
		voice_client.is_playing()
	else :
		ctx.channel.send("รอแปปนึงน้าาา ^^")
		return

@bot.command()
async def play(ctx,url):
	  
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except:
        await ctx.send("The bot is not connected to a voice channel.")


@bot.command()
async def discon(ctx):
	await ctx.channel.send("เค้าไปแล้วน้าา ^^")
	await ctx.voice_client.disconnect()

@bot.command()
async def con(ctx):
	channel = ctx.author.voice.channel
	voice_client = get(bot.voice_clients,guild = ctx.guild)

	if voice_client == None :
		ctx.channel.send("เค้ามาแล้ววว")
		await channel.connect()
		voice_client = get(bot.voice_clients, guild = ctx.guild)
		source = FFmpegPCMAudio('Music_Youtube_Free.wav')

    

@bot.command()
async def st(ctx):
	voice_client = get(bot.voice_clients,guild = ctx.guild)

	if voice_client == None :
		await ctx.chanel.send("เค้าไม่ได้เปิดเพลงอยู่นะตอนนี้อ่ะะะะ")
		return 

	if voice_client != ctx.author.voice.channel :
		await ctx.channel.send("เธอไม่ได้อยู่ห้องที่เค้าเปิดเพลง เพราะงั้นสั่งเค้าไม่ด้ายยยยย")
	
	voice_client.stop()
	await ctx.channel.send("โอเค เค้าหยุดเปิดเพลงแล้ววว(stop)")

@bot.command()
async def pu(ctx):
	voice_client = get(bot.voice_clients,guild = ctx.guild)

	if voice_client == None :
		await ctx.chanel.send("เค้าไม่ได้เปิดเพลงอยู่นะตอนนี้อ่ะะะะ")
		return 

	if voice_client != ctx.author.voice.channel :
		await ctx.channel.send("เธอไม่ได้อยู่ห้องที่เค้าเปิดเพลง เพราะงั้นสั่งเค้าไม่ด้ายยยยย")
	
	voice_client.pause()
	await ctx.channel.send("โอเค เค้าหยุดเปิดเพลงแล้ววว(pause)")

@bot.command()
async def rs(ctx):
	voice_client = get(bot.voice_clients,guild = ctx.guild)

	if voice_client == None :
		await ctx.chanel.send("เค้าไม่ได้เปิดเพลงอยู่นะตอนนี้อ่ะะะะ")
		return 

	if voice_client != ctx.author.voice.channel :
		await ctx.channel.send("เธอไม่ได้อยู่ห้องที่เค้าเปิดเพลง เพราะงั้นสั่งเค้าไม่ด้ายยยยย")
	
	voice_client.resume()
	await ctx.channel.send("โอเค เค้าเปิดเพลงให้ฟังต่อแล้ววว(resume)")

@bot.event 
async def on_message(data):
	global blackup_num_hungry

	if data.content == "cpe":
		num = randomResult(5)
		await data.channel.send((result_check[num]))

	elif "หิว" in data.content : 
		num = randomResult(5)
		blackup_num_hungry = num
		await data.channel.send(result_hungry[num])

	elif "เบื่อ" in data.content :
		num = randomResult(6)
		await data.channel.send(result_bored[num])

	elif "เหงา" in data.content :
		num = randomResult(6)
		await data.channel.send(result_bored[num])


	await bot.process_commands(data)

@bot.command()
async def ts(ctx):
	channel = ctx.author.voice.channel
	voice_client = get(bot.voice_clients,guild = ctx.guild)

	if voice_client == None :
		ctx.channel.send("เค้ามาแล้ววว")
		await channel.connect()
		voice_client = get(bot.voice_clients, guild = ctx.guild)
		voice_client.play(discord.FFmpegPCMAudio('Music_Youtube_Free.wav'))
		#await channel.disconnect()


@bot.event 
async def on_ready():
	print ("bot cpe ready ! ")


bot.run('MTA2OTE5MDk4MjczNTc3NzgwMg.GR7z5l.f39qs05QL0EvFJUiFI4yvQ6Mnxa3329vGt7kDM')
#MTAwMDAzNzk4OTI5NDAyNjgzMg.GAuo7P.bfqCT3wnARN9PQQRxcinXMhc3DYVynQVYWNlBk