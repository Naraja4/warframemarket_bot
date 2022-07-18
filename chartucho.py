import requests
import urllib3, discord, json
from discord.ext import tasks
urllib3.disable_warnings()

#Discord bot token
TOKEN = ''

def requestShellShockData():
    URL='https://api.warframe.market/v1/items/shell_shock/orders'
    response=requests.get(URL, verify=False)
    return response.json()

def requestSupraVandalData():
    URL='https://api.warframe.market/v1/items/supra_vandal/orders'
    response=requests.get(URL, verify=False)
    return response.json()

def requestfissureData():
    URL='https://api.warframestat.us/pc/fissures'
    response=requests.get(URL, verify=False)
    return response.json()


def shell():
     
    t=requestShellShockData()
    low=999999999
    for i in range(len(t['payload']['orders'])):
        if low>t['payload']['orders'][i]['platinum'] and t['payload']['orders'][i]['user']['status']=='ingame' and t['payload']['orders'][i]['order_type']=='sell' and t['payload']['orders'][i]['region']=='en':
            low=t['payload']['orders'][i]['platinum']

    msg='El precio de **catucho eléctrico** ahora mismo es de: '+str(low)+' de platino.'

    return msg,low

def supra():
    
    t=requestSupraVandalData()
    low=999999999
    for i in range(len(t['payload']['orders'])):
        if low>t['payload']['orders'][i]['platinum'] and t['payload']['orders'][i]['user']['status']=='ingame' and t['payload']['orders'][i]['order_type']=='sell' and t['payload']['orders'][i]['region']=='en':
            low=t['payload']['orders'][i]['platinum']

    msg='El precio de la **supra vándalo** ahora mismo es de: '+str(low)+' de platino.'

    return msg,low

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    with open('warframemarket.json', "rb") as f: 
        data = json.load(f)
        data['cartucho']=-1
        data['supra']=-1
        with open("warframemarket.json", "w") as jsonFile:
            json.dump(data,jsonFile)
    
    with open('fisuras.json', "rb") as f: 
        data = json.load(f)
        data=[]
        with open("fisuras.json", "w") as jsonFile:
            json.dump(data,jsonFile)



@tasks.loop(seconds=10)
async def mytask():
    with open('warframemarket.json', "rb") as f: 
        data = json.load(f)

    channel = await client.fetch_channel(981292041529073700)

    msg,priceshell=shell()
    msg2,pricesupra=supra()

    if priceshell!=data['cartucho']:
        await channel.send(msg)
        data['cartucho']=priceshell
        with open("warframemarket.json", "w") as jsonFile:
            json.dump(data,jsonFile)
    if pricesupra!=data['supra']:
        await channel.send(msg2)
        data['supra']=pricesupra
        with open("warframemarket.json", "w") as jsonFile:
            json.dump(data,jsonFile)

@tasks.loop(seconds=10)
async def fissure():
    with open('fisuras.json', "rb") as f: 
        data = json.load(f)
    
    channel = await client.fetch_channel(981292041529073700)
    t=requestfissureData()
    temp=[]

    for i in range(len(t)):
        temp.append(t[i]['nodeKey'])
        if t[i]['nodeKey'] not in data:
            if t[i]['missionKey']=='Disruption' and t[i]['isStorm']==False:
                msg='Hay una disrupción **'+t[i]['tier']+'**.'+' Termina en: **'+t[i]['eta']+'**.'
                await channel.send(msg)
                data.append(t[i]['nodeKey'])
                with open("fisuras.json", "w") as jsonFile:
                    json.dump(data,jsonFile)

            elif t[i]['missionKey']=='Capture' and t[i]['isStorm']==False:
                msg='Hay una captura **'+t[i]['tier']+'** en **'+t[i]['nodeKey']+'**.'+' Termina en: **'+t[i]['eta']+'**.'
                await channel.send(msg)
                data.append(t[i]['nodeKey'])
                with open("fisuras.json", "w") as jsonFile:
                    json.dump(data,jsonFile)

            elif t[i]['missionKey']=='Extermination' and t[i]['isStorm']==False:
                msg='Hay un exterminio **'+t[i]['tier']+'** en **'+t[i]['nodeKey']+'**.'+' Termina en: **'+t[i]['eta']+'**.'
                await channel.send(msg)
                data.append(t[i]['nodeKey'])
                with open("fisuras.json", "w") as jsonFile:
                    json.dump(data,jsonFile)
    
    for node in data:
        if node not in temp:
            msg='La fisura **'+node+'** ha terminado.'
            await channel.send(msg)
            data.remove(node)
            with open("fisuras.json", "w") as jsonFile:
                json.dump(data,jsonFile)


fissure.start()
mytask.start()

client.run(TOKEN)