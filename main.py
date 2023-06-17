import os
import discord
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import lyricsgenius

load_dotenv()

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

genius = lyricsgenius.Genius(os.getenv('tokenGenius'))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Comando Olá. Comando para verificar as mensagens enviadas no chat. Biblioteca do Discord.py
    if message.content.startswith('$hello'):
        # Comando para o BOT enviar algo no chat. Biblioteca do Discord.py
        await message.channel.send('Hello!')

    # Comando para mostrar uma foto do artista. Aqui é usado bastante a biblioteca do Spotipy
    if message.content.startswith('$ShowTheArtist'):

        # Verifica se a mensagem após o camndo de acionamento.
        if len(message.content[len('$ShowTheArtist'):]) > 0:

            # Adiciona a mensagem que esta após o comando de acionamento a variavel "name"
            name = message.content[len('$ShowTheArtist'):]

            # Busca pelo artista no banco de dados.
            results = spotify.search(q='artist:' + name, type='artist')
            items = results['artists']['items']

            if len(items) > 0:
                artist = items[0]
                await message.channel.send(artist['images'][0]['url'])
            else:
                await message.channel.send('Artist not found')
            
        else:
            await message.channel.send("Type an artist")

    # Comando para mostrar a letra de uma musica.Aqui é usado bastante a biblioteca do lyricsgenius.
    if message.content.startswith('$ShowTheLyrics '):
        if len(message.content[len('$ShowTheLyrics '):]) > 0:
            musicLyric = message.content[len('$ShowTheLyrics '):]

            # Busca pela letra da musina no banco de dados.
            song = genius.search_song(musicLyric)

            if song:

                # Mensagens a cima de 2000 caracteres não podem ser enviadas.
                if len(song.lyrics) > 1997:
                    song.lyrics = song.lyrics[:1997] + "..."
                    await message.channel.send(song.lyrics)
                else:
                    await message.channel.send(song.lyrics)

            else:
                await message.channel.send("Song lyrics dont find")

        else:
            await message.channel.send("Type a song")

client.run(os.getenv('tokenSpotify'))