from flask import Flask, request, redirect
from gmusicapi import Mobileclient
import twilio.twiml
from classes import Song, User

PLAYLISTNAME = 'textJam'
isPlaylistCreated = False


api = Mobileclient()
# implement a solution to have user login
logged_in = api.login('jusanden7@gmail.com', 'zpewalrdeytbdhmu', Mobileclient.FROM_MAC_ADDRESS)
if (logged_in):
    print("logged in")
else:
    print("Log in failed, please verify login details")


def parseQuery(query):
    results = api.search_all_access(query, 10)
    parsedID = results['song_hits'][0]['track']['storeId']
    parsedTitle = results['song_hits'][0]['track']['title']
    parsedArtist = results['song_hits'][0]['track']['artist']
    parsedLength = results['song_hits'][0]['track']['durationMillis']
    return Song(parsedTitle, parsedArtist, parsedLength, parsedID)


def createPlaylist():
    global playlistID
    global isPlaylistCreated

    playlistID = api.create_playlist(PLAYLISTNAME, 'none', True)
    isPlaylistCreated = True


def deletePlaylist():
    global isPlaylistCreated

    if (isPlaylistCreated):
        api.delete_playlist(playlistID)
        isPlaylistCreated = False
    else:
        print("Playlist Not Created Yet")


def addSong(song):
    if (isPlaylistCreated):
        api.add_songs_to_playlist(playlistID, song.songID)
        return 1
    else:
        return 0


s = parseQuery('Animal Collective')
print(s.title)
print(s.artist)
