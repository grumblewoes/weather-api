import discord
import requests
import json as JSON
import os
import datetime
from dotenv import load_dotenv


load_dotenv()
client = discord.Client()

stateCodes = {
    "al":"alabama",
    "ak":"alaska",
    "az":"arizona",
    "ar":"arkansas",
    "ca":"california",
    "co":"colorado",
    "ct":"connecticut",
    "de":"delaware",
    "fl":"florida",
    "ga":"georgia",
    "hi":"hawaii",
    "id":"idaho",
    "il":"illinois",
    "in":"indiana",
    "ia":"iowa",
    "ks":"kansas",
    "ky":"kentucky",
    "la":"louisiana",
    "me":"maine",
    "md":"maryland",
    "ma":"massachusetts",
    "mi":"michigan",
    "mn":"minnesota",
    "ms":"mississippi",
    "mo":"missouri",
    "mt":"montana",
    "ne":"nebraska",
    "nv":"nevada",
    "nh":"newhampshire",
    "nj":"newjersey",
    "nm":"newmexico",
    "ny":"newyork",
    "nc":"northcarolina",
    "nd":"northdakota",
    "oh":"ohio",
    "ok":"oklahoma",
    "or":"oregon",
    "pa":"pennsylvania",
    "ri":"rhodeisland",
    "sc":"southcarolina",
    "sd":"southdakota",
    "tn":"tennessee",
    "tx":"texas",
    "ut":"utah",
    "vt":"vermont",
    "va":"virginia",
    "wa":"washington",
    "wv":"westvirginia",
    "wi":"wisconsin",
    "wy":"wyoming"
}

def weatherTypes(weather):
    switcher = {
        "scattered clouds": "scattered clouds.",
        "clear sky": "clear skies.",
        "few clouds": "few clouds.",
        "broken clouds": "light cloud cover.",
        "overcast clouds": "overcast clouds.",
        "light rain": "light rain.",
        "heavy intensity rain": "heavy rain.",
        "moderate rain": "rain.",
        
      
        
    }
    return switcher.get(weather, "[new weather type, go check the json].")


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$weather"):
        commands = message.content[8:]
        commands = commands.strip().split(" ")
        
        #fetching json
        location = "http://api.openweathermap.org/data/2.5/weather?q=" + str(commands[0]) + "," + str(stateCodes[commands[1]]).lower() + "&appid=a5c08a7648cc59fe41aaccae29a672c4&units=imperial"
        jsonText = requests.get(location).text
        json = JSON.loads(jsonText) #translates str into json format
        
        #determine grammar for weather type
        weather = weatherTypes(json["weather"][0]["description"])
        report = "In "+ commands[0].capitalize() + ", it is currently " + str(round(json["main"]["temp"])) + "° F, with " + weather
        
        print(json)
        await message.channel.send(report)
       


    if message.content.startswith("$forecast"):
        commands = message.content[9:]
        commands = commands.strip().split(" ")

        #fetching json
        location = "http://api.openweathermap.org/data/2.5/forecast?q=" + str(commands[0]) + "," + str(stateCodes[commands[1]]).lower() + "&appid=a5c08a7648cc59fe41aaccae29a672c4&units=imperial"
        jsonText = requests.get(location).text
        json = JSON.loads(jsonText) #translates str into json format
        
        #times needed
        startDay = datetime.datetime.today()
        day2= startDay + datetime.timedelta(days=1)
        day3= day2 + datetime.timedelta(days=1)
        day4= day3 + datetime.timedelta(days=1)
        day5= day4 + datetime.timedelta(days=1)
        
        #embed setup
        embed = discord.Embed(title="Weather Forecast", colour=0x87CEEB, timestamp=datetime.datetime.now())
        embed.add_field(name=startDay.strftime('%a'), value=str(round(json["list"][0]["main"]["temp"]))+ "° F", inline=True)
        embed.add_field(name=day2.strftime("%a"), value=str(round(json["list"][7]["main"]["temp"]))+ "° F", inline=True)
        embed.add_field(name=day3.strftime("%a"), value=str(round(json["list"][15]["main"]["temp"]))+ "° F", inline=True)
        embed.add_field(name=day4.strftime("%a"), value=str(round(json["list"][23]["main"]["temp"]))+ "° F", inline=True)
        embed.add_field(name=day5.strftime("%a"), value=str(round(json["list"][31]["main"]["temp"]))+ "° F", inline=True)
        embed.set_footer(text="Weather Man", icon_url="https://static.vecteezy.com/system/resources/previews/000/450/015/original/cloud-vector-icon.jpg")
        
        print(json)
        await message.channel.send(embed=embed)
    

client.run(os.getenv("BOT_TOKEN"))

#api.openweathermap.org/data/2.5/weather?q={city name},{state code}&appid={API key}