import discord
from discord.ext import commands
from youtube_dl import YoutubeDL


# Class containing the logic for the music bot
# @author Shayne Mintling


class music(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                               'options': '-vn'}

        self.vc = None

    # method to search YouTube
    # returns url and title
    def yt_search(self, ctx):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % ctx, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    # method to play the next song in the queue
    def next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            url2 = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(url2, **self.FFMPEG_OPTIONS), after=lambda e: self.next())
        else:
            self.is_playing = False

    # method to play music
    async def play_m(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            url2 = self.music_queue[0][0]['source']

            if self.vc is None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc is None:
                    await ctx.send("Can't connect")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(url2, **self.FFMPEG_OPTIONS), after=lambda e: self.next())

        else:
            self.is_playing = False

    # commands to control the bot
    # use key character and command name in text channel to use command
    @commands.command()
    async def play(self, ctx, *url):
        q = " ".join(url)
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("Join a voice channel")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.yt_search(q)
            if type(song) == type(True):
                await ctx.send("try something else")
            else:
                await ctx.send(":thumbsup:")
                self.music_queue.append([song, voice_channel])

                if not self.is_playing:
                    await self.play_m(ctx)

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()
        self.music_queue = []

    @commands.command()
    async def pause(self):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()

    @commands.command()
    async def queue(self, ctx):
        ret_val = ""

        for i in range(0, len(self.music_queue)):
            if i > 15:
                break
            ret_val += self.music_queue[i][0]['title'] + ', '

        if ret_val != "":
            await ctx.send(ret_val)
        else:
            await ctx.send("Nothing in queue")

    @commands.command()
    async def skip(self, ctx):
        if self.vc is not None and self.vc:
            self.vc.stop()
            await self.play_m(ctx)

    # feature not yet implemented
    @commands.command()
    async def np(self, ctx):
        await ctx.send("This doesn't work yet")

    @commands.command()
    async def clean(self, ctx):
        await ctx.purge("!play" + "!leave" + "!queue" + "!np" + "!clean")

    @commands.command()
    async def commands(self, ctx):
        await ctx.send("!play LINK or title - to play a song or just !play to unpause the bot\n"
                       "!pause - to pause the song\n"
                       "!skip - to skip the current song\n"
                       "!leave - to make the bot disconnect\n"
                       "!queue - to see the queue\n"
                       "!np - to see now playing\n"
                       "!clean - to remove all commands for chat\n")


def setup(client):
    client.add_cog(music(client))
