# Doppelganger Discord Bot

The Doppelganger Bot is a chat bot that uses a fine-tuned [GPT-2-simple model](https://github.com/minimaxir/gpt-2-simple) to imitate the speech style of a singular person up to even a whole group of people.





# Table of Contents
- [Requirements](#Requirements)
- [Overview](#Overview)
- [Usage](#Usage)
- [Notes](#Notes)


# Requirements
This Discord bot uses your own Discord API bot token to function. Make sure your go to their website and create one before starting. Also do not forget to add it to your servers.

To use this bot, the following packages and installations with these exact versions are required:
- tensorflow 1.15.2
- cuda 10.0
- cuDNN 7.4
- python 3.6
- gpt-2-simple

You may need to use an environment with downgraded versions of your current installs.

# Overview
Doppelganger Bot comes with several commands and features. Some commands are required to be sent in the particular channel you want a reply in while other commands can be sent anywhere for ease of use. Some of the major features are:

- Discord status changing
- Message history scraping
- Guess the message roulette
- Replying with context-based generated text

# Usage
For first time usage:
1. Ensure you have all necessary packages and installations at the correct versions.
2. Download doppelganger_bot.py, doppelganger_train.py, and [discord_message_parser.py]() to the same directory.
3. Choose your preferred settings and fill in your information in doppelganger_bot.py (things like bot token, command prefix, users to pull data from, keyword activation).
4. Run doppelganger_bot.py.
5. Type the !scrape command in a channel that the bot has access to. Make sure your channel ids are loaded in doppelganger_bot.py before doing this.
6. Run discord_message_cleaner.py with the resultant json from the scrape command to get a new master json and train.txt
7. Follow the instructions in doppelganger_train.py with your new train.txt file and run the first block of code followed by the second seperately.
8. Re-run doppelganger_bot.py with the new master.json and model.
9. Type the !load command in any discord channel that the bot has access to on start-up.

The bot is now ready to be used. 

For subsequent uses, only steps 8 and 9 are needed.

To retrain the model for a new set of people, repeat steps 1-9.

# Notes
Please note that it is possible for the model to output profane language and other obscenities. The output is entirely dependent on the input to the model so please be aware of what you train the model on. 

Use Doppelganger Bot at your own discretion.

## Credits/References
Credits and references for data, installations, ideas, code, and/or inspiration

1. https://github.com/minimaxir/gpt-2-simple


Thank you for reading.
