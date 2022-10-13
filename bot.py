import logging
import aiohttp as aiohttp
import yaml
from telethon import TelegramClient, events
from telethon.tl.types import InputWebDocument

with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

client = TelegramClient(**config['telethon_settings']).start(bot_token=config['bot_token'])
api_key = config['api_key']
maxResult = config['maxResult']
session = aiohttp.ClientSession()
f.close()


async def items_request(type: str, search_query: str):
    async with session.get('https://www.googleapis.com/youtube/v3/search', params={'part': 'snippet',
                                                                                   'q': search_query,
                                                                                   'maxResult': maxResult,
                                                                                   'type': type,
                                                                                   'key': api_key}) as response:
        resp = await response.json()
        return resp['items']


@client.on(events.NewMessage(pattern='/start'))
async def help_plox(event):
    await event.reply('Available switches:'
                      '\n.v for videos'
                      '\n.p for playlists'
                      '\n.c for channels'
                      '\nPattern: `@youtubehandybot <switch> <search query>`')


@client.on(events.InlineQuery())
async def reply(event):
    if event.text.startswith('.v'):
        items = await items_request(type='video', search_query=event.text[2:])
        await event.answer([event.builder.article(title=item['snippet']['title'],
                                                  description=f"Published by: {item['snippet']['channelTitle']}",
                                                  thumb=InputWebDocument(
                                                      url=item['snippet']['thumbnails']['default']['url'],
                                                      size=0,
                                                      mime_type='image/jpg',
                                                      attributes=[]),
                                                  text=f"https://www.youtube.com/watch?v={item['id']['videoId']}") for
                            item in items])
    elif event.text.startswith('.p'):
        items = await items_request(type='playlist', search_query=event.text[2:])
        await event.answer([event.builder.article(title=item['snippet']['title'],
                                                  description=f"Published by: {item['snippet']['channelTitle']}",
                                                  thumb=InputWebDocument(
                                                      url=item['snippet']['thumbnails']['default']['url'],
                                                      size=0,
                                                      mime_type='image/jpg',
                                                      attributes=[]),
                                                  text=f"https://www.youtube.com/playlist?list={item['id']['playlistId']}")
                            for item in items])
    elif event.text.startswith('.c'):
        items = await items_request(type='channel', search_query=event.text[2:])
        await event.answer([event.builder.article(title=item['snippet']['title'],
                                                  description=f"Published by: {item['snippet']['channelTitle']}",
                                                  thumb=InputWebDocument(
                                                      url=item['snippet']['thumbnails']['default']['url'],
                                                      size=0,
                                                      mime_type='image/jpg',
                                                      attributes=[]),
                                                  text=f"https://www.youtube.com/channel/{item['id']['channelId']}")
                            for item in items])
    else:
        await event.answer([event.builder.article('No switch detected', text='Available switches:'
                                                                             '\n.v for videos'
                                                                             '\n.p for playlists'
                                                                             '\n.c for channels'
                                                                             '\nPattern: `@youtubehandybot <switch> <search query>`')])


client.start()
client.run_until_disconnected()
