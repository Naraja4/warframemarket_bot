import requests
import urllib3, discord, json
from discord.ext import tasks
urllib3.disable_warnings()

#Discord bot token
TOKEN = ''
with open('b.json', "rb") as jsonFile: 
        data = json.load(jsonFile)



def requestData(item):
    URL='https://api.warframe.market/v1/items/'+item+'/orders'
    response=requests.get(URL, verify=False)
    return response.json()


def shell(item):
     
    t=requestData(item)
    low=999999999
    for i in range(len(t['payload']['orders'])):
        if low>t['payload']['orders'][i]['platinum'] and t['payload']['orders'][i]['user']['status']=='ingame' and t['payload']['orders'][i]['order_type']=='sell' and t['payload']['orders'][i]['region']=='en':
            low=t['payload']['orders'][i]['platinum']

    msg='El precio de **'+item+'** ahora mismo es de: '+str(low)+' de platino.'

    return msg,low


client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):

    channel = message.channel
    
    if message.content[:4]=='!add':
            item=message.content[5:]

            if item not in data.keys():
                data[item]=0
                with open("b.json", "w") as jsonFile:
                    json.dump(data,jsonFile)
                await channel.send('Se ha agregado el item a la lista.')
    
    if message.content[:7]=='!remove':
            item=message.content[8:]

            if item in data.keys():
                data.pop(item)
                with open("b.json", "w") as jsonFile:
                    json.dump(data,jsonFile)
                await channel.send('Se ha eliminado el item de la lista.')
                
@tasks.loop(seconds=10)
async def mytask():
    channel = await client.fetch_channel(981292041529073700)

    if len(data.keys())>0:
        for item in data.keys():
            msg,priceshell=shell(item)

            if priceshell!=data[item]:
                await channel.send(msg)
                data[item]=priceshell
                with open("b.json", "w") as jsonFile:
                    json.dump(data,jsonFile)

mytask.start()

client.run(TOKEN)
