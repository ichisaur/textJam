
from gmusicapi import Mobileclient
from twilio.rest import TwilioRestClient
from classes import Song, Message
import threading
import time


loginID = #Google Account Username
authToken = #Google Account Password


account_sid = #Twilio Account SID
auth_token = #Twilio Auth Token


PLAYLISTNAME = 'textJam'
defaultQuery1 = "Mr. Brightside"
defaultQuery2 = "Ho Hey"
twilioNumber = #Twilio Number


currentSongLength = 15
stopPlayback = False
isPlaylistCreated = False
listOfMessages = []


class timerThread (threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID

    def run(self):
        global stopPlayback
        global currentSongLength
        while not stopPlayback:
            temp = currentSongLength
            currentSongLength = int(topVotedSong(songList).duration)/5000
            done = addTopSong(songList)
            if done:
                time.sleep(temp)


def parseQuery(query):
    results = api.search_all_access(query, 15)
    if results['song_hits'] == []:
        return 'error'
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


def parseMessage(message):
    ssid = message.sid
    fromNum = message.from_
    query = message.body
    return Message(ssid, query, fromNum)


def filterMessages(number):
    messages = client.messages.list(to=number)
    newMessages = []
    for i in messages:
        if i.status == 'received':
            newMessages.append(parseMessage(i))
        else:
            print(i.status)
    for i in newMessages:
        client.messages.delete(i.mSSID)
    return newMessages


def sendConfirmationMessage(song, number):
    if int(song.votes) == int(topVotedSong(songList).votes):
        body = "Hi, you have successfully voted for " + song.title + " by " + song.artist + ". It's currently set to be queued up next!"
    else:
        numberMore = int(topVotedSong(songList).votes) - int(song.votes)
        body = "Hi, you have successfully voted for " + song.title + " by " + song.artist + ". It needs " + str(numberMore) + " vote(s) to queued up next!"
    to = number
    from_ = twilioNumber
    client.messages.create(body=body, to=to, from_=from_)
    print("sent message to " + number)



def loopFunction():
    stopPlayback = False
    while not stopPlayback:
        newMessages = filterMessages(twilioNumber)
        for i in newMessages:
            query = i.query
            if query == '#stop':
                stopPlayback = True
                print('stopped')
                break

            s = parseQuery(query)
            if s == 'error':
                client.messages.create(body="Sorry, we couldn't find your song.", to=i.fromNum, from_=twilioNumber)
                print("sent message to " + i.fromNum)
                time.sleep(1)
            else:
                if not listContains(s, songList):
                    songList.append(s)
                    s.vote()
                else:
                    s = returnSong(s, songList)
                    if not s.votes == -1:
                        s.vote()
                print(s.title)
                print(s.votes)
                sendConfirmationMessage(s, i.fromNum)
    time.sleep(1)

client = TwilioRestClient(account_sid, auth_token)

api = Mobileclient()
logged_in = api.login(loginID, authToken, Mobileclient.FROM_MAC_ADDRESS)

if (logged_in):
    print("log in success")
else:
    print("Log in failed, please verify login details")

deleteMessages = client.messages.list(to=twilioNumber)
for i in deleteMessages:
    ssid = i.sid
    client.messages.delete(ssid)
print('previous queue cleared')

createPlaylist()
print('playlist created')

songList = []
queuedSongList = []

s1 = parseQuery(defaultQuery1)
s2 = parseQuery(defaultQuery2)

songList.append(s1)
songList.append(s2)
addSong(s1)
s1.votes = -1
s2.votes = 10

currentSongLength = int(s1.duration)/5000

delayLoop = timerThread(1)
delayLoop.start()

loopFunction()

deletePlaylist()
