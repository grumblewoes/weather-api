import discord
import requests
import json as JSON
import os
import datetime
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
        
        #fetching json
        location = "http://api.openweathermap.org/data/2.5/weather?q=" + str(commands[0]) + "," + str(commands[1]) + "&appid=a5c08a7648cc59fe41aaccae29a672c4&units=imperial"
        jsonText = requests.get(location).text
        json = JSON.loads(jsonText) #translates str into json format
        await message.channel.send("In "+ commands[0].capitalize() + ", it is currently " + str(json["main"]["temp"]) + " degrees.")
        print("In " + commands[0].capitalize() + ", it is currently " + str(json["main"]["temp"]) + " degrees.")

    if message.content.startswith("$forecast"):
        commands = message.content[9:]
        commands = commands.strip().split(" ")

        #fetching json
        location = "http://api.openweathermap.org/data/2.5/forecast?q=" + str(commands[0]) + "," + str(commands[1]) + "&appid=a5c08a7648cc59fe41aaccae29a672c4&units=imperial"
        jsonText = requests.get(location).text
        json = JSON.loads(jsonText) #translates str into json format
        
        #times needed
        startDay = datetime.datetime.today()
        day2= startDay + datetime.timedelta(days=1)
        day3= day2 + datetime.timedelta(days=1)
        day4= day3 + datetime.timedelta(days=1)
        day5= day4 + datetime.timedelta(days=1)
        
        #embed setup
        embed = discord.Embed(title="Weather Forecast", colour=0x87CEEB)
        embed.set_author(name="Weather Man", icon_url="https://static.vecteezy.com/system/resources/previews/000/450/015/original/cloud-vector-icon.jpg")
        embed.add_field(name=startDay.strftime('%a'), value=str(json["list"][0]["main"]["temp"])+ "° F", inline=True)
        embed.add_field(name=day2.strftime('%a'), value=str(json["list"][7]["main"]["temp"])+ "° F", inline=True)
        embed.add_field(name=day3.strftime('%a'), value=str(json["list"][15]["main"]["temp"])+ "° F", inline=True)
        embed.add_field(name=day4.strftime('%a'), value=str(json["list"][23]["main"]["temp"])+ "° F", inline=True)
        embed.add_field(name=day5.strftime('%a'), value=str(json["list"][31]["main"]["temp"])+ "° F", inline=True)
        
        
        await message.channel.send(embed=embed)
        print("Temp of " + str(json["list"][0]["main"]["temp_min"]))
        #"High of " + str(json[3]["main"]["temp_max"]) + ", low of " + str(json[3]["main"]["temp_max"])
    

client.run(os.getenv("BOT_TOKEN"))

#api.openweathermap.org/data/2.5/weather?q={city name},{state code}&appid={API key}