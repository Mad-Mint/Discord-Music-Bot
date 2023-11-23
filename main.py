import discord
from discord.ext import commands
import music
import info


def main():
    cogs = [music]

    client = commands.Bot(command_prefix='!', intents=discord.Intents.all(), case_insensitive=True)

    for i in range(len(cogs)):
        cogs[i].setup(client)

    client.run(info.botToken)


if __name__ == '__main__':
    main()
