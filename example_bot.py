import discord
import requests
import json as JSON
import os
from dotenv import load_dotenv


load_dotenv()
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith("$weather"):
        commands = message.content[8:]
        commands = commands.strip().split(" ")
        await message.channel.send(commands)

        location = "http://api.openweathermap.org/data/2.5/weather?q=" + str(commands[0]) + "," + str(commands[1]) + "&appid=a5c08a7648cc59fe41aaccae29a672c4&units=imperial"
        #await message.channel.send(requests.get(location).text)
        jsonText = requests.get(location).text
        json = JSON.loads(jsonText) #translates str into json format
        await message.channel.send("It is " + str(json["main"]["temp"]) + " degrees out")
        
        

client.run(os.getenv("BOT_TOKEN"))

#api.openweathermap.org/data/2.5/weather?q={city name},{state code}&appid={API key}