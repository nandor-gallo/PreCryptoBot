import discord
import requests
import json
import os
from dotenv import load_dotenv
# Insert your Discord bot token and CoinMarketCap API key here
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
API_KEY = os.getenv('API_KEY')


# Authenticate your bot token with Discord
intents = discord.Intents.all()
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Playground!'
    )

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

# Listen for the $price command and retrieve the latest Bitcoin price from CoinMarketCap
@client.event
async def on_message(message):
    if message.content.startswith('$help'):
        await message.channel.send("```Here are a list of commands you can use: \n\n$price [symbol] - find out latest price of crpyto\n$change [symbol] - find out latest coin changes within 24H 7D 30D```")

    if message.content.startswith('$price'):
        # Split the user's message into tokens and extract the desired cryptocurrency name
        tokens = message.content.split()
        if len(tokens) < 2:
            await message.channel.send('Please specify a cryptocurrency name')
            return
        crypto_name = tokens[1]

        # Make an API call to CoinMarketCap to retrieve the latest cryptocurrency data
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        params = {'symbol': crypto_name.upper()}
        headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': API_KEY}
        response = requests.get(url, headers=headers, params=params)
        data = json.loads(response.text)

        # Extract the latest cryptocurrency price and send it back to the user
        if 'status' in data and data['status']['error_code'] == 400:
            await message.channel.send(f'Error: {data["error"]["error_message"]}')
        else:
            crypto_data = data['data'][crypto_name.upper()]
            crypto_price = crypto_data['quote']['USD']['price']
            await message.channel.send(f"{crypto_name.upper()} price: ${crypto_price:.8f}")

    if message.content.startswith('$change'):
        # Split the user's message into tokens and extract the desired cryptocurrency name
        tokens = message.content.split()
        if len(tokens) < 2:
            await message.channel.send('Please specify a cryptocurrency name')
            return
        crypto_name = tokens[1]

        # Make an API call to CoinMarketCap to retrieve the latest cryptocurrency data
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        params = {'symbol': crypto_name.upper()}
        headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': API_KEY}
        response = requests.get(url, headers=headers, params=params)
        data = json.loads(response.text)

        # Extract the latest cryptocurrency price and send it back to the user
        if 'status' in data and data['status']['error_code'] == 400:
            await message.channel.send(f'Error: {data["error"]["error_message"]}')
        else:
            crypto_data = data['data'][crypto_name.upper()]
            crypto_change1D = crypto_data['quote']['USD']['percent_change_24h']
            crypto_change7D = crypto_data['quote']['USD']['percent_change_7d']
            crypto_change30D = crypto_data['quote']['USD']['percent_change_30d']
            await message.channel.send(f"{crypto_name.upper()} changes after [ 24H {crypto_change1D:.2f}% | 7 Days {crypto_change7D:.2f}% | 30 Days {crypto_change30D}]")

# Run the bot
client.run(TOKEN)
