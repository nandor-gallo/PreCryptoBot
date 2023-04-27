import discord
import requests
import json

# Insert your Discord bot token and CoinMarketCap API key here
TOKEN = 'MTA5OTkxNzk5MTE1MzUwNDMxNg.GSXY_F.PQyvVpE5uvYrF2eQcnX9eLSmh4WwxaE03g9pZk'
API_KEY = '58f62acb-e381-4829-8f66-767a10ffdf73'

# Authenticate your bot token with Discord
intents = discord.Intents.all()
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

# Listen for the $price command and retrieve the latest Bitcoin price from CoinMarketCap
@client.event
async def on_message(message):
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
            await message.channel.send(f"{crypto_name.upper()} price: ${crypto_price:.2f}")

# Run the bot
client.run(TOKEN)
