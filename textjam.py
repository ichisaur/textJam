from flask import Flask, request, redirect
from gmusicapi import Mobileclient
from classes import Song, User
import threading
import time
from threading import Timer

PLAYLISTNAME = 'textJam'
isPlaylistCreated = False
loginID = 'jusanden7@gmail.com'
authToken = 'zpewalrdeytbdhmu'
defaultQuery1 = "Mr. Brightside"
defaultQuery2 = "Ho Hey"
currentSongLength = 15
stopPlayback = False


class timerThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        global stopPlayback
        global currentSongLength
        while not stopPlayback:
            temp = currentSongLength
            currentSongLength = int(topVotedSong(songList).duration)/1000
            done = addTopSong(songList)
            if done:           
                time.sleep(temp)


def parseQuery(query):
    results = api.search_all_access(query, 50)
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


def listContains(song, listOfSongs):
    for i in listOfSongs:
        if i.songID == song.songID:
            return True
    return False


def topVotedSong(listOfSongs):
    topSong = listOfSongs[0]
    for i in listOfSongs:
        if i.votes >= topSong.votes:
            topSong = i
    return topSong


def addTopSong(songList):
    if topVotedSong(songList).votes > -1:
        api.add_songs_to_playlist(playlistID, topVotedSong(songList).songID)
        topVotedSong(songList).votes = -1
        return 1
    else:
        return 0


def returnSong(song, songList):
    for i in songList:
        if song.songID == i.songID:
            return i
    else:
        return song


def loopFunction():
    # currentSongLength = (int(topVotedSong(songList).duration))/10000
    global stopPlayback
    stopPlayback = False
    while not stopPlayback:
        userQuery = input('Input song keyword: ')
        if userQuery == '#stop':
            stopPlayback = True
            break
        s = parseQuery(userQuery)
        if not listContains(s, songList):
            songList.append(s)
            s.vote()
        else:
            s = returnSong(s, songList)
            if not s.votes == -1:
                s.vote()
        print(s.votes)




api = Mobileclient()
# implement a solution to have user login
logged_in = api.login(loginID, authToken, Mobileclient.FROM_MAC_ADDRESS)
if (logged_in):
    print("logged in")
else:
    print("Log in failed, please verify login details")


createPlaylist()

songList = []
queuedSongList = []

s1 = parseQuery(defaultQuery1)
s2 = parseQuery(defaultQuery2)
songList.append(s1)
songList.append(s2)
addSong(s1)
s2.votes = 10
currentSongLength = int(s1.duration)/1000
delayLoop = timerThread(1)
delayLoop.start()

loopFunction()

deletePlaylist()

