# DISCORDIFY

## Convert your python code to a discord bot in less than 5 minutes!
![Discordify Logo](./docs/Discordify-Logo.png)

## Quickstart - Running the example

Clone this repository.
```sh
git clone https://github.com/arumugam666/discordify
```

Install the repository.
```sh
cd discordify && pip3 install .
```

Create a discord app, and a bot under the application. Get the token
corresponding to this app. This can be done at the
[discord developer site](https://discord.com/developers/applications/)

You can follow [this](https://www.writebots.com/discord-bot-token) tutorial to
get a bot token.

Create the token file.
```sh
touch tests_integration/token.dcfy
```

Put your token in the token file.

Run the bot.
```sh
cd tests_integration
run_discordify_app.py ./config.json ./token.dcfy
```

## Convert python code to a discord bot

Ensure that you're in the application directory

Create config files
```sh
create_config.py
```

Edit the config file and the token file appropriately.

Run app
```sh
run_discordify_app.py .discord-config/config.json .discord-config/token.dcfy
```