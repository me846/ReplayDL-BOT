# What is this bot?

This repository enables a bot to control the client externally in an environment where replay files can be successfully downloaded. 
The bot sends a download request to the server side and posts the obtained replay file. 
As a result, users whose replay files are corrupted and unviewable can obtain and view a normal replay file through the bot

## Setup Instructions

1.Create a .env file  
  ・Add DISCORD_TOKEN=`<Your Bot Token>`  
  ・Copy and paste your bot token from here: https://discord.com/developers/applications/  

2.Modify replayDL.py  
  ・Change the `JP1` in the filename `JP1-{game_id}.rofl` on line 34 to your region's code, which you can identify from the name of your replay files

3.Start the Bot
  ・Run `python main.py` to start the bot.

### Executed with a slash command  

There is a `game_id` option available when you use `/replaydl`.   
The game ID can be obtained from the client's match history.    
When executed, the bot sends a download request for the replay file to the RIOT server through the client and retrieves it

#### License

This project is licensed under the [MIT License](https://github.com/me846/neon-chat/blob/master/LICENSE)
