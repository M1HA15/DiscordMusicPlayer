import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import platform
import asyncio
import json
import logging
from datetime import datetime
import random
import os

def format_duration(seconds):
    minutes, sec = divmod(int(seconds), 60)
    return f"{minutes:02d}:{sec:02d}"

def create_embed(title, description, color=discord.Color.purple()):
    embed = discord.Embed(title=title, description=description, color=color)
    return embed

def create_category_pages(category_title, commands_list):
    lines = []
    for cmd in commands_list:
        if cmd.hidden:
            continue
        alias_text = f" (alias: {', '.join(cmd.aliases)})" if cmd.aliases else ""
        lines.append(f"`{cmd.name}`{alias_text} – {cmd.help or 'Fără descriere'}")
    pages = []
    chunk_size = 6
    for i in range(0, len(lines), chunk_size):
        page_desc = "\n".join(lines[i:i+chunk_size])
        embed = create_embed(category_title, f"Prefixul curent: `{PREFIX}`\n\n{page_desc}", discord.Color.purple())
        pages.append(embed)
    return pages

try:
    with open("settings.json", "r", encoding="utf-8") as f:
        config = json.load(f)
except Exception as e:
    config = {}
    logging.error(f"Nu s-a putut încărca settings.json: {e}")

OWNER_ID = int(config.get("owner_id", 0))
ALLOWED_GUILDS = [str(g) for g in config.get("guild_ids", [])]
TIMEOUT_MINUTES = int(config.get("timeout", 0))
TIMEOUT_SECONDS = TIMEOUT_MINUTES * 60

TOKEN = os.getenv("DISCORD_TOKEN") or config.get("token")
PREFIX = config.get("prefix", "!")
STATUS_TYPE = config.get("status_type", "").lower()
STATUS_MESSAGE = config.get("status_message", "")
ALT_PREFIX = config.get("alt_prefix", "")
DEFAULT_VOLUME = float(config.get("volume", 0.5))

if not TOKEN:
    logger = logging.getLogger("discord")
    logger.error("Token-ul nu este setat! Asigură-te că ai definit variabila de mediu DISCORD_TOKEN sau ai adăugat tokenul în settings.json")
    exit(1)

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("logs.txt", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

async def paginate(ctx, pages, timeout=60):
    message = await ctx.send(embed=pages[0])
    if len(pages) == 1:
        return
    await message.add_reaction("◀")
    await message.add_reaction("▶")

    def check(reaction, user):
        return user == ctx.author and reaction.message.id == message.id and str(reaction.emoji) in ["◀", "▶"]

    current_page = 0
    while True:
        try:
            reaction, user = await ctx.bot.wait_for("reaction_add", timeout=timeout, check=check)
        except asyncio.TimeoutError:
            break
        else:
            if str(reaction.emoji) == "▶":
                current_page = (current_page + 1) % len(pages)
            elif str(reaction.emoji) == "◀":
                current_page = (current_page - 1) % len(pages)
            try:
                await message.edit(embed=pages[current_page])
                await message.remove_reaction(reaction.emoji, user)
            except Exception as e:
                logger.error(f"Eroare la navigarea paginilor: {e}")

class CustomHelpCommand(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        owner_cmds = []
        music_cmds = []
        other_cmds = []
        for command in self.context.bot.commands:
            if command.hidden:
                continue
            if command.name in ["logs", "gaccept"]:
                owner_cmds.append(command)
            elif command.name in [
                "start", "join", "play", "pause", "resume", "skip", "voteskip",
                "queue", "nowplaying", "songlink", "youtubelink", "volume",
                "loop", "clear", "shuffle", "remove", "songinfo",
                "createplaylist", "addtoplaylist", "viewplaylist", "listplaylists",
                "removeplaylist", "playplaylist"
            ]:
                music_cmds.append(command)
            else:
                other_cmds.append(command)
        pages = []
        if owner_cmds:
            pages.extend(create_category_pages("🔧 Comenzi Owner", owner_cmds))
        if music_cmds:
            pages.extend(create_category_pages("🎵 Comenzi Muzică", music_cmds))
        if other_cmds:
            pages.extend(create_category_pages("📌 Alte Comenzi", other_cmds))
        if pages:
            await paginate(self.context, pages)
        else:
            await self.get_destination().send("Nu există comenzi disponibile.")

    async def send_cog_help(self, cog):
        embed = create_embed(
            f"Comenzi din categoria {cog.qualified_name} 🎶",
            f"Prefixul curent: `{PREFIX}`\n{cog.description or 'Fără descriere'}",
            discord.Color.purple()
        )
        for command in cog.get_commands():
            if command.hidden:
                continue
            alias_text = f" (alias: {', '.join(command.aliases)})" if command.aliases else ""
            embed.add_field(
                name=f"`{command.name}`{alias_text}",
                value=command.help or "Fără descriere",
                inline=False
            )
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        alias_text = f" (alias: {', '.join(command.aliases)})" if command.aliases else ""
        embed = create_embed(
            f"Ajutor pentru comanda `{command.name}`{alias_text}",
            f"Prefix: `{PREFIX}`\n{command.help or 'Fără descriere'}",
            discord.Color.purple()
        )
        await self.get_destination().send(embed=embed)

prefixes = [PREFIX]
if ALT_PREFIX:
    prefixes.append(ALT_PREFIX)
bot = commands.Bot(command_prefix=prefixes, intents=intents, description="github.com/M1HA15", help_command=CustomHelpCommand())

@bot.check
async def check_guild(ctx):
    if not ctx.guild:
        return False
    if str(ctx.guild.id) in ALLOWED_GUILDS:
        return True
    return False

def is_dj():
    async def predicate(ctx):
        if ctx.author.id == OWNER_ID:
            return True
        guild_roles = config.get("dj_roles", {})
        guild_dj_id = guild_roles.get(str(ctx.guild.id))
        if guild_dj_id and any(role.id == int(guild_dj_id) for role in ctx.author.roles):
            return True
        raise commands.CheckFailure("Nu ai permisiunile necesare! (Rol DJ necesar)")
    return commands.check(predicate)

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == bot.user.id:
        if before.channel and not after.channel:
            guild_id = member.guild.id
            if guild_id in players:
                del players[guild_id]
                logger.info(f"MusicPlayer pentru guild {guild_id} șters pe on_voice_state_update.")

async def update_global_presence():
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            active_players = [p for p in players.values() if p.current]
            if STATUS_TYPE == "streaming":
                activity = discord.Streaming(name=STATUS_MESSAGE, url=STATUS_MESSAGE)
            elif STATUS_TYPE == "watching":
                activity = discord.Activity(type=discord.ActivityType.watching, name=STATUS_MESSAGE)
            elif STATUS_TYPE == "listening":
                activity = discord.Activity(type=discord.ActivityType.listening, name=STATUS_MESSAGE)
            elif STATUS_TYPE == "playing" and STATUS_MESSAGE:
                activity = discord.Game(name=STATUS_MESSAGE)
            else:
                if active_players:
                    activity = discord.Game(name=active_players[0].current.title)
                elif STATUS_MESSAGE:
                    activity = discord.Game(name=STATUS_MESSAGE)
                else:
                    activity=discord.Game(name="Lătrat pe beat, sunt câine lăchit 🐶")
            await bot.change_presence(status=discord.Status.online, activity=activity)
            if len(active_players) == 1:
                await bot.change_presence(
                    status=discord.Status.dnd,
                    activity=discord.Activity(type=discord.ActivityType.listening, name=active_players[0].current.title)
                )
            elif len(active_players) > 1:
                await bot.change_presence(
                    status=discord.Status.dnd,
                    activity=discord.Game(name=f"Câinele mixează pe {len(active_players)} servere 🎧🐶")
                )
        except Exception as e:
            logger.error(f"Eroare la actualizarea prezenței: {e}")
        await asyncio.sleep(5)

@bot.event
async def on_ready():
    now = datetime.now().strftime("%H:%M:%S, %d-%m-%Y")
    logger.info(f"Botul a pornit la ora {now}")
    bot.loop.create_task(update_global_presence())
    print(f"Bot conectat ca {bot.user}")

ytdl_format_options = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0"
}
ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin",
    "options": "-vn"
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=DEFAULT_VOLUME):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")
        self.thumbnail = data.get("thumbnail")
        self.duration = data.get("duration", 0)

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()
        try:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        except Exception as e:
            raise RuntimeError(f"Eroare la extragerea informațiilor: {e}")
        if data is None:
            raise RuntimeError("Nu am putut găsi nicio sursă pentru acest URL.")
        if "entries" in data:
            data = data["entries"][0]
        stream_url = data.get("url") if stream else ytdl.prepare_filename(data)
        logger.info(f"Sursa extrasă: {data.get('title', 'necunoscut')}")
        try:
            return cls(discord.FFmpegPCMAudio(stream_url, **ffmpeg_options), data=data)
        except Exception as e:
            raise RuntimeError(f"Eroare la redare ffmpeg: {e}")

class MusicPlayer:
    def __init__(self, ctx):
        self.bot = ctx.bot
        self._ctx = ctx
        self.guild = ctx.guild
        self.text_channel = ctx.channel
        self.voice = ctx.voice_client
        self.queue = asyncio.Queue()
        self.queue_lock = asyncio.Lock()
        self.current = None
        self.current_start_time = None
        self.skip_votes = set()
        self.votes = set()
        self.volume = DEFAULT_VOLUME
        self.loop_flag = False
        self.player_task = bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        while not self.destroyed:
            if not self.queue.empty():
                async with self.queue_lock:
                    source = await self.queue.get()
                self.current = source
                self.current_start_time = datetime.now()
                self.voice.play(source, after=lambda e: logger.error(f"MusicPlayer: {e}") if e else None)
                while self.voice.is_playing() or self.voice.is_paused():
                    await asyncio.sleep(1)
            else:
                await asyncio.sleep(1)

    async def destroy(self, guild):
        self.destroyed = True
        if self.player_task:
            self.player_task.cancel()
        try:
            if guild.voice_client:
                guild.voice_client.stop()
                await guild.voice_client.disconnect()
        except Exception as e:
            logger.error(f"Eroare la deconectare: {e}")
        if guild.id in players:
            del players[guild.id]
        logger.info(f"MusicPlayer pentru guild {guild.id} eliminat.")

players = {}

def get_player(ctx):
    if ctx.guild.id in players and ctx.voice_client is None:
        del players[ctx.guild.id]
    player = players.get(ctx.guild.id)
    if not player:
        player = MusicPlayer(ctx)
        players[ctx.guild.id] = player
    else:
        player.text_channel = ctx.channel
    return player

@bot.command(name="start", help="Connect the bot and start playback automatically")
async def start(ctx):
    if not ctx.author.voice:
        await ctx.send(embed=create_embed("❌ Eroare", "Trebuie să fii într-un canal de voce.", discord.Color.red()))
        return
    channel = ctx.author.voice.channel
    try:
        if not ctx.voice_client:
            await channel.connect()
            await asyncio.sleep(0.5)
        else:
            await ctx.voice_client.move_to(channel)
    except Exception as e:
        logger.error(f"Eroare la conectare: {e}")
        await ctx.send(embed=create_embed("❌ Eroare", f"Nu pot să mă conectez: {e}", discord.Color.red()))
        return
    if ctx.guild.id in players:
        await players[ctx.guild.id].destroy(ctx.guild)
    get_player(ctx)
    await ctx.send(embed=create_embed("🤖 Bot Activat!", f"Conectat la **{channel.name}**.\nAdaugă piesele și le voi reda automat!", discord.Color.green()))

@bot.command(name="join", aliases=["j"], help="Connect the bot to the voice channel")
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        try:
            if not ctx.voice_client:
                await channel.connect()
                await asyncio.sleep(0.5)
            else:
                await ctx.voice_client.move_to(channel)
            await ctx.send(embed=create_embed("🎵 Conectare reușită", f"Botul s-a conectat la **{channel.name}**.", discord.Color.blue()))
        except Exception as e:
            logger.error(f"Eroare la join: {e}")
            await ctx.send(embed=create_embed("❌ Eroare", f"Nu am putut să mă conectez: {e}", discord.Color.red()))
    else:
        await ctx.send(embed=create_embed("❌ Eroare", "Trebuie să fii într-un canal de voce.", discord.Color.red()))

@bot.command(name="disconnect", aliases=["dc","stop"], help="Disconnect the bot from the voice channel")
async def disconnect(ctx):
    if ctx.voice_client:
        try:
            await ctx.voice_client.disconnect()
            if ctx.guild.id in players:
                await players[ctx.guild.id].destroy(ctx.guild)
            await ctx.send(embed=create_embed("🚪 Deconectare", "Botul s-a deconectat.", discord.Color.red()))
        except Exception as e:
            logger.error(f"Eroare la disconnect: {e}")
            await ctx.send(embed=create_embed("❌ Eroare", f"Eroare la deconectare: {e}", discord.Color.red()))
    else:
        await ctx.send(embed=create_embed("❌ Eroare", "Botul nu este conectat.", discord.Color.red()))

@bot.command(name="play", aliases=["p"], help="Add a track to the queue and play automatically")
async def play(ctx, *, query: str):
    if "open.spotify.com" in query:
        await ctx.send(embed=create_embed("❌ Eroare", "Suportul pentru Spotify este dezactivat.", discord.Color.red()))
        return
    if not ctx.voice_client:
        await join(ctx)
        await asyncio.sleep(0.5)
    player = get_player(ctx)
    try:
        source = await YTDLSource.from_url(query, loop=bot.loop, stream=True)
    except Exception as e:
        await ctx.send(embed=create_embed("❌ Play Error", f"Nu am putut procesa cererea: {e}", discord.Color.red()))
        return
    if not source or not source.url:
        await ctx.send(embed=create_embed("❌ Eroare", "Nu am putut obține o sursă validă.", discord.Color.red()))
        return
    await player.queue.put(source)
    await ctx.send(embed=create_embed("🎶 Track Added", f"**{source.title}** ({format_duration(source.duration)}) a fost adăugată în coadă!", discord.Color.purple()))

@bot.command(name="playlist", help="Play a playlist (playlist URL)")
async def playlist(ctx, *, query: str):
    if not ctx.voice_client:
        await join(ctx)
        await asyncio.sleep(0.5)
    player = get_player(ctx)
    loop_ = bot.loop
    opts = ytdl_format_options.copy()
    opts['noplaylist'] = False
    pl_ytdl = youtube_dl.YoutubeDL(opts)
    try:
        data = await loop_.run_in_executor(None, lambda: pl_ytdl.extract_info(query, download=False))
    except Exception as e:
        await ctx.send(embed=create_embed("❌ Playlist Error", f"Nu am putut procesa cererea: {e}", discord.Color.red()))
        logger.error(f"Eroare la playlist: {e}")
        return
    if 'entries' not in data:
        await ctx.send(embed=create_embed("❌ Eroare", "Nu a fost găsit niciun playlist sau acesta nu este valid.", discord.Color.red()))
        return
    count = 0
    for entry in data['entries']:
        if entry:
            try:
                source = await YTDLSource.from_url(entry['webpage_url'], loop=loop_, stream=True)
                await player.queue.put(source)
                count += 1
            except Exception as e:
                logger.error(f"Eroare la adăugarea unei piese din playlist: {e}")
                continue
    await ctx.send(embed=create_embed("📃 Playlist adăugat", f"Playlist-ul a fost adăugat cu **{count}** piese în coadă.", discord.Color.green()))

@bot.command(name="pause", help="Pause playback")
async def pause(ctx):
    vc = ctx.voice_client
    if vc and vc.is_playing():
        vc.pause()
        await ctx.send(embed=create_embed("⏸️ Pauză", "Redarea a fost pusă în pauză.", discord.Color.orange()))
    else:
        await ctx.send(embed=create_embed("❌ Eroare", "Nicio piesă nu se redă.", discord.Color.red()))

@bot.command(name="resume", help="Resume playback")
async def resume(ctx):
    vc = ctx.voice_client
    if vc and vc.is_paused():
        vc.resume()
        await ctx.send(embed=create_embed("▶️ Continuare", "Redarea a fost reluată.", discord.Color.orange()))
    else:
        await ctx.send(embed=create_embed("❌ Eroare", "Nu există nicio piesă în pauză.", discord.Color.red()))

@bot.command(name="skip", aliases=["s"], help="Skip the current song (DJ required)")
@is_dj()
async def skip(ctx):
    vc = ctx.voice_client
    if vc and vc.is_playing():
        vc.stop()
        await ctx.send(embed=create_embed("⏭️ Skip", "Piesa a fost sărită.", discord.Color.gold()))
    else:
        await ctx.send(embed=create_embed("❌ Eroare", "Nicio piesă nu se redă.", discord.Color.red()))

@bot.command(name="voteskip", aliases=["vskip","vs"], help="Vote to skip the current song")
async def voteskip(ctx):
    player = get_player(ctx)
    vc = ctx.voice_client
    if not vc or not vc.is_playing():
        await ctx.send(embed=create_embed("❌ Eroare", "Nicio piesă nu se redă.", discord.Color.red()))
        return
    if ctx.author.id in player.votes:
        await ctx.send(embed=create_embed("❌ Eroare", "Ai votat deja pentru skip.", discord.Color.red()))
        return
    player.votes.add(ctx.author.id)
    voice_channel = vc.channel
    total_members = len([m for m in voice_channel.members if not m.bot])
    required_votes = max(1, total_members // 2)
    if len(player.votes) >= required_votes:
        vc.stop()
        await ctx.send(embed=create_embed("⏭️ Skip Aprobat", "Votul a fost aprobat!", discord.Color.gold()))
        player.votes.clear()
    else:
        await ctx.send(embed=create_embed("🗳️ Vot pentru skip", f"Ai votat pentru skip. {len(player.votes)}/{required_votes} voturi necesare.", discord.Color.blue()))

@bot.command(name="queue", help="Show the playback queue")
async def queue_(ctx):
    player = get_player(ctx)
    if player.queue.empty():
        await ctx.send(embed=create_embed("📭 Coada goală", "Nu există piese în coadă.", discord.Color.blurple()))
    else:
        async with player.queue_lock:
            upcoming = list(player.queue._queue)
        lines = [f"{i+1}. **{track.title}** ({format_duration(track.duration)})" for i, track in enumerate(upcoming)]
        pages = []
        chunk_size = 10
        for i in range(0, len(lines), chunk_size):
            chunk = "\n".join(lines[i:i+chunk_size])
            pages.append(create_embed("🎶 Coada de redare", chunk, discord.Color.blurple()))
        await paginate(ctx, pages)

@bot.command(name="nowplaying", aliases=["np"], help="Show currently playing song")
async def nowplaying(ctx):
    player = get_player(ctx)
    if player.current:
        elapsed = (datetime.now() - player.current_start_time).seconds if player.current_start_time else 0
        embed = create_embed("🎵 Acum redă", f"**{player.current.title}** [{format_duration(elapsed)}/{format_duration(player.current.duration)}]", discord.Color.green())
        if player.current.thumbnail:
            embed.set_thumbnail(url=player.current.thumbnail)
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=create_embed("❌ Eroare", "Momentan nu se redă nicio piesă.", discord.Color.red()))

@bot.command(name="volume", help="Set the current volume (0-100)")
async def volume(ctx, vol: int):
    vc = ctx.voice_client
    if not vc or not isinstance(vc.source, discord.PCMVolumeTransformer):
        await ctx.send(embed=create_embed("❌ Eroare", "Nu există sursă sau nu se poate modifica volumul.", discord.Color.red()))
        return
    if vol < 0 or vol > 100:
        await ctx.send(embed=create_embed("❌ Eroare", "Volumul trebuie să fie între 0 și 100.", discord.Color.red()))
        return
    vc.source.volume = vol / 100
    player = get_player(ctx)
    player.volume = vol / 100
    config["volume"] = player.volume
    try:
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        logger.error(f"Eroare la salvarea volumului: {e}")
    await ctx.send(embed=create_embed("🔊 Volum Actualizat", f"Volumul a fost setat la {vol}%.", discord.Color.green()))

@bot.command(name="loop", help="Toggle loop of the current song")
async def loop(ctx):
    player = get_player(ctx)
    player.loop_flag = not player.loop_flag
    status = "activat" if player.loop_flag else "dezactivat"
    await ctx.send(embed=create_embed("🔄 Loop", f"Loop-ul a fost {status}.", discord.Color.magenta()))

@bot.command(name="clear", help="Clear the playback queue (DJ required)")
@is_dj()
async def clear(ctx):
    player = get_player(ctx)
    async with player.queue_lock:
        player.queue = asyncio.Queue()
    await ctx.send(embed=create_embed("🗑️ Coada Resetată", "Coada a fost resetată.", discord.Color.dark_red()))

@bot.command(name="shuffle", help="Shuffle the songs in the queue (DJ required)")
@is_dj()
async def shuffle(ctx):
    player = get_player(ctx)
    async with player.queue_lock:
        if player.queue.empty():
            await ctx.send(embed=create_embed("📭 Coada goală", "Nu există piese pentru amestecare.", discord.Color.red()))
            return
        qlist = list(player.queue._queue)
        random.shuffle(qlist)
        player.queue = asyncio.Queue()
        for s in qlist:
            await player.queue.put(s)
    await ctx.send(embed=create_embed("🔀 Coada Amestecată", "Piesele au fost amestecate.", discord.Color.gold()))

@bot.command(name="remove", help="Remove a track from the queue by position (DJ required)")
@is_dj()
async def remove(ctx, index: int):
    player = get_player(ctx)
    async with player.queue_lock:
        if player.queue.empty():
            await ctx.send(embed=create_embed("📭 Coada goală", "Nu există piese în coadă.", discord.Color.red()))
            return
        qlist = list(player.queue._queue)
        if index < 1 or index > len(qlist):
            await ctx.send(embed=create_embed("❌ Eroare", "Index invalid.", discord.Color.red()))
            return
        removed = qlist.pop(index - 1)
        player.queue = asyncio.Queue()
        for s in qlist:
            await player.queue.put(s)
    await ctx.send(embed=create_embed("🗑️ Piesă Eliminată", f"Piesa **{removed.title}** a fost eliminată.", discord.Color.orange()))

@bot.command(name="songlink", aliases=["slink"], help="Show the current song's link")
async def songlink(ctx):
    player = get_player(ctx)
    if player.current:
        await ctx.send(embed=create_embed("🔗 Track Link", f"[{player.current.title}]({player.current.url})", discord.Color.green()))
    else:
        await ctx.send(embed=create_embed("❌ Eroare", "Momentan nu se redă nicio piesă.", discord.Color.red()))

@bot.command(name="youtubelink", aliases=["ytlink"], help="Show the current song's YouTube link")
async def ytlink(ctx):
    player = get_player(ctx)
    if player.current:
        yt_url = player.current.data.get("webpage_url")
        if yt_url:
            await ctx.send(embed=create_embed("🔗 YouTube Link", f"[{player.current.title}]({yt_url})", discord.Color.green()))
        else:
            await ctx.send(embed=create_embed("❌ Eroare", "Nu am găsit link-ul YouTube.", discord.Color.red()))
    else:
        await ctx.send(embed=create_embed("❌ Eroare", "Momentan nu se redă nicio piesă.", discord.Color.red()))

@bot.command(name="songinfo", aliases=["sinfo"], help="Show information about the current song")
async def songinfo(ctx):
    player = get_player(ctx)
    if player.current:
        stream_url = player.current.url
        yt_url = player.current.data.get("webpage_url", "Niciun link")
        embed = create_embed("ℹ️ Informații Piesă", f"**{player.current.title}**", discord.Color.blue())
        embed.add_field(name="Stream link", value=stream_url, inline=False)
        embed.add_field(name="YouTube link", value=yt_url, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=create_embed("❌ Eroare", "Momentan nu se redă nicio piesă.", discord.Color.red()))

def load_playlists():
    if not os.path.exists("playlists.json"):
        return {}
    try:
        with open("playlists.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Eroare la încărcarea playlist-urilor: {e}")
        return {}

def save_playlists(playlists):
    try:
        with open("playlists.json", "w", encoding="utf-8") as f:
            json.dump(playlists, f, indent=4)
    except Exception as e:
        logger.error(f"Eroare la salvarea playlist-urilor: {e}")

@bot.command(name="createplaylist", aliases=["cpl","createpl"], help="Create a personal playlist (max. 5 playlists)")
async def createplaylist(ctx, *, name: str):
    playlists = load_playlists()
    user_id = str(ctx.author.id)
    count = sum(1 for pl in playlists.values() if pl.get("owner") == user_id)
    if count >= 5:
        await ctx.send(embed=create_embed("❌ Eroare", "Ai atins limita de 5 playlist-uri.", discord.Color.red()))
        return
    for pl in playlists.values():
        if pl.get("owner") == user_id and pl.get("name", "").lower() == name.lower():
            await ctx.send(embed=create_embed("❌ Eroare", "Playlistul există deja.", discord.Color.red()))
            return
    new_id = max((int(k) for k in playlists.keys()), default=0) + 1
    playlists[str(new_id)] = {"owner": user_id, "name": name, "songs": []}
    save_playlists(playlists)
    await ctx.send(embed=create_embed("✅ Playlist Created", f"Playlist **{name}** a fost creat cu ID-ul `{new_id}`.", discord.Color.green()))

@bot.command(name="addtoplaylist", aliases=["atpl","addtopl"], help="Add a track to a personal playlist (max. 40 tracks)")
async def addtoplaylist(ctx, playlist_identifier: str, *, query: str):
    playlists = load_playlists()
    if playlist_identifier.isdigit():
        pl_id = playlist_identifier
        if pl_id not in playlists:
            await ctx.send(embed=create_embed("❌ Eroare", "Playlistul nu există.", discord.Color.red()))
            return
    else:
        pl_id = None
        for pid, pl in playlists.items():
            if pl.get("name", "").lower() == playlist_identifier.lower():
                pl_id = pid
                break
        if not pl_id:
            await ctx.send(embed=create_embed("❌ Eroare", "Playlistul nu a fost găsit.", discord.Color.red()))
            return
    if playlists[pl_id].get("owner") != str(ctx.author.id):
        await ctx.send(embed=create_embed("❌ Eroare", "Nu ai permisiuni pentru a modifica acest playlist.", discord.Color.red()))
        return
    if len(playlists[pl_id].get("songs", [])) >= 40:
        await ctx.send(embed=create_embed("❌ Eroare", "Playlistul a atins limita de 40 de piese.", discord.Color.red()))
        return
    playlists[pl_id].setdefault("songs", []).append(query)
    save_playlists(playlists)
    name = playlists[pl_id].get("name", "Fără nume")
    await ctx.send(embed=create_embed("✅ Track Added", f"Piesa a fost adăugată la playlistul **{name}** (ID: {pl_id}).", discord.Color.green()))

@bot.command(name="listplaylists", aliases=["lpl","listpl"], help="List available playlists")
async def listplaylists(ctx):
    playlists = load_playlists()
    if not playlists:
        await ctx.send(embed=create_embed("ℹ️ Playlists", "Nu există playlist-uri create.", discord.Color.blue()))
        return
    desc = ""
    for pid, pl in playlists.items():
        owner_name = "Necunoscut"
        try:
            owner = await bot.fetch_user(int(pl.get("owner", "0")))
            if owner:
                owner_name = owner.name
        except:
            pass
        name = pl.get("name", "Fără nume")
        songs = pl.get("songs", [])
        desc += f"**ID:** `{pid}` | **Name:** {name} | **Tracks:** {len(songs)} | **Owner:** {owner_name}\n"
    await ctx.send(embed=create_embed("ℹ️ Playlists", desc, discord.Color.blue()))

@bot.command(name="viewplaylist", aliases=["vpl","viewpl"], help="Show all songs in a playlist")
async def viewplaylist(ctx, identifier: str):
    playlists = load_playlists()
    if identifier.isdigit():
        pl_id = identifier
        if pl_id not in playlists:
            await ctx.send(embed=create_embed("❌ Eroare", "Playlistul nu există.", discord.Color.red()))
            return
    else:
        pl_id = None
        for pid, pl in playlists.items():
            if pl.get("name", "").lower() == identifier.lower():
                pl_id = pid
                break
        if not pl_id:
            await ctx.send(embed=create_embed("❌ Eroare", "Playlistul nu a fost găsit.", discord.Color.red()))
            return
    songs = playlists[pl_id].get("songs", [])
    name = playlists[pl_id].get("name", "Fără nume")
    if not songs:
        await ctx.send(embed=create_embed(f"ℹ️ Playlist: {name}", "Playlistul este gol.", discord.Color.blue()))
        return
    lines = [f"{i+1}. {song}" for i, song in enumerate(songs)]
    pages = []
    chunk_size = 10
    for i in range(0, len(lines), chunk_size):
        chunk = "\n".join(lines[i:i+chunk_size])
        pages.append(create_embed(f"ℹ️ Playlist: {name} (ID: {pl_id})", chunk, discord.Color.blue()))
    await paginate(ctx, pages)

@bot.command(name="removeplaylist", aliases=["removepl","rmpl"], help="Delete a personal playlist")
async def removeplaylist(ctx, identifier: str):
    playlists = load_playlists()
    if identifier.isdigit():
        pl_id = identifier
        if pl_id not in playlists:
            await ctx.send(embed=create_embed("❌ Eroare", "Playlistul nu există.", discord.Color.red()))
            return
    else:
        pl_id = None
        for pid, pl in playlists.items():
            if pl.get("name", "").lower() == identifier.lower():
                pl_id = pid
                break
        if not pl_id:
            await ctx.send(embed=create_embed("❌ Eroare", "Playlistul nu a fost găsit.", discord.Color.red()))
            return
    if playlists[pl_id].get("owner") != str(ctx.author.id):
        await ctx.send(embed=create_embed("❌ Eroare", "Nu ai permisiunea de a șterge acest playlist.", discord.Color.red()))
        return
    name = playlists[pl_id].get("name", "Fără nume")
    del playlists[pl_id]
    save_playlists(playlists)
    await ctx.send(embed=create_embed("✅ Playlist Deleted", f"Playlist **{name}** (ID: {pl_id}) a fost șters.", discord.Color.green()))

@bot.command(name="playplaylist", aliases=["playpl"], help="Automatically play a playlist (can belong to another user)")
async def playplaylist(ctx, identifier: str):
    playlists = load_playlists()
    if identifier.isdigit():
        pl_id = identifier
        if pl_id not in playlists:
            await ctx.send(embed=create_embed("❌ Eroare", "Playlistul nu există.", discord.Color.red()))
            return
    else:
        pl_id = None
        for pid, pl in playlists.items():
            if pl.get("name", "").lower() == identifier.lower():
                pl_id = pid
                break
        if not pl_id:
            await ctx.send(embed=create_embed("❌ Eroare", "Playlistul nu a fost găsit.", discord.Color.red()))
            return
    songs = playlists[pl_id].get("songs", [])
    name = playlists[pl_id].get("name", "Fără nume")
    if not songs:
        await ctx.send(embed=create_embed("ℹ️ Playlist gol", "Acest playlist nu are piese.", discord.Color.blue()))
        return
    if not ctx.voice_client:
        await join(ctx)
        await asyncio.sleep(0.5)
    player = get_player(ctx)
    count = 0
    for query in songs:
        try:
            source = await YTDLSource.from_url(query, loop=bot.loop, stream=True)
            await player.queue.put(source)
            count += 1
        except Exception as e:
            logger.error(f"Eroare la adăugarea piesei din playlist: {e}")
            continue
    await ctx.send(embed=create_embed("✅ Playlist Played", f"{count} tracks from **{name}** (ID: {pl_id}) have been added to the queue!", discord.Color.green()))

@bot.command(name="logs", help="Show last logs (Owner Only)")
@commands.is_owner()
async def logs(ctx, lines: int = 15):
    try:
        if os.path.exists("logs.txt"):
            with open("logs.txt", "r", encoding="utf-8") as f:
                all_lines = f.readlines()
        else:
            await ctx.send(embed=create_embed("ℹ️ Logs", "Log file does not exist.", discord.Color.blue()))
            return
        content = "".join(all_lines[-lines:])
        if len(content) > 1900:
            content = content[-1900:]
        await ctx.send(embed=create_embed("📜 Last logs", f"```{content}```", discord.Color.dark_gold()))
    except Exception as e:
        await ctx.send(embed=create_embed("❌ Eroare", f"Eroare la citirea log-urilor: {e}", discord.Color.red()))

@bot.command(name="ping", help="Shows latency and technical information")
async def ping(ctx):
    latency_ms = bot.latency * 1000
    embed = create_embed("🏓 Ping", f"Latency: **{latency_ms:.2f} ms**\ndiscord.py: {discord.__version__}\nPython: {platform.python_version()}", discord.Color.green())
    embed.add_field(name="🔗 Links", value="[GitHub Profile](https://github.com/M1HA15)", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="gaccept", help="Accept a server (Owner Only)")
@commands.is_owner()
async def gaccept(ctx, server_id: str):
    if server_id not in config.get("guild_ids", []):
        config.setdefault("guild_ids", []).append(server_id)
        try:
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            await ctx.send(embed=create_embed("Server Acceptat", f"Serverul {server_id} a fost acceptat.", discord.Color.green()))
        except Exception as e:
            logger.error(f"Eroare la salvarea setărilor: {e}")
            await ctx.send(embed=create_embed("❌ Eroare", f"Nu am putut salva setările: {e}", discord.Color.red()))
    else:
        await ctx.send(embed=create_embed("Server Existent", f"Serverul {server_id} este deja acceptat.", discord.Color.orange()))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=create_embed("❌ Eroare", "Un argument necesar lipsește.", discord.Color.red()))
    elif isinstance(error, commands.NotOwner):
        await ctx.send(embed=create_embed("🚫 Acces interzis", "Comanda este rezervată proprietarului.", discord.Color.red()))
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(embed=create_embed("🚫 Acces interzis", str(error), discord.Color.red()))
    else:
        logger.error(f"Eroare necunoscută: {error}")
        await ctx.send(embed=create_embed("❌ Eroare", f"A apărut o eroare: `{error}`", discord.Color.red()))

bot.run(TOKEN)