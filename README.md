# ReplayDL-BOT

This repository enables a bot to control the League of Legends client externally in an environment where replay files can be successfully downloaded. The bot sends a download request to the server side and posts the obtained replay file. As a result, users whose replay files are corrupted and unviewable can obtain and view a normal replay file through the bot.

## Installation and Setup

To get started with the bot, follow these steps:

1. **Download and Extract the Bot**
   - Download the latest release of the ReplayDL_BOT from the [Releases page](https://github.com/me846/ReplayDL-BOT/releases).
   - Extract the downloaded zip file.

2. **Configure the Bot**
   - Open the `config.ini` file located in the extracted directory.
   - Obtain your bot token from the [Discord Developer Portal](https://discord.com/developers/applications/) and paste it into the `config.ini` file under `BOT_TOKEN`:
     ```
     BOT_TOKEN = Your Bot Token
     ```

3. **Set Your Region**
   - In the `config.ini` file, set the `REGION` to match the region of your League of Legends client. The available regions are:
     ```
     REGION = BR1
     REGION = EUN1
     REGION = EUW1
     REGION = JP1
     REGION = KR
     REGION = LA1
     REGION = LA2
     REGION = NA1
     REGION = OC1
     REGION = TR1
     REGION = RU
     REGION = PH2
     REGION = SG2
     REGION = TH2
     REGION = TW2
     REGION = VN2
     ```

4. **Run the Bot**
   - Ensure your League of Legends client is running.
   - Start the bot by running the executable (`ReplayDL_BOT.exe`).

   If the bot starts successfully, you will see the following message:
```BOT#1111 is online  1 slash commands```

### Executed with a slash command  

There is a `game_id` option available when you use `/replaydl`.   
The game ID can be obtained from the client's match history.    
When executed, the bot sends a download request for the replay file to the RIOT server through the client and retrieves it

#### License

This project is licensed under the [MIT License](https://github.com/me846/neon-chat/blob/master/LICENSE)
