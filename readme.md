# Discord Music Bot
    This is Version one discord.py and ffmpeg have been updated and this bot no longer works on latest versions.
## About This Project
    This project was made when YouTube disabled a music bot my server used. I decided this would be a fun 
    project to learn the basics of Python and asynchronous programming.
## Getting Started
### Prerequisites
    Python
    discord.py 1.7.3
        PyNaCl
    youtube_dl
    FFMPEG
### Installation
    Install required packages by running requirements.cmd
		OR 
	Manually install these packages
	To install discord.py run:
		pip install --user discord==1.7.3
	To install PyNaCl run:
		pip install --user pynacl==1.4.0
	To install YouTube_dl run:
		pip install youtube_dl
	To install FFMPEG run:
		pip install --user FFMPEG==1.4
### Building
    In main.py on line 14 change "info.botToken" to your Discord bot Token. More information here: 
    https://discordpy.readthedocs.io/en/stable/discord.html
	Once the packages have been installed you can now run the bot.
### Usage
	Here are a list of commands used to control the bot
	!play LINK or title - to play a song or just !play to unpause the bot
    !pause - to pause the song
    !skip - to skip the current song
    !leave - to make the bot disconnect
    !queue - to see the queue
    !np - to see now playing
    !clean - to remove all commands for chat
### How to Contribute
1. Clone the repo and create a new branch: git clone git@github.com:Mad-Mint/Discord-Music-Bot.git
2. Make changes and test
3. Submit a Pull Request with a comprehensive description of changes 
