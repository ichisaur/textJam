class Song():

    """represents the songs that are passed to gplay music"""

    

    def __init__(self, title, songID):
        self.title = title
        self.songID = songID
        self.votes = 0
    

    def vote(self): 
        self.votes += 1

class User():

    """Stores user data"""


    def __init__(self, phoneNumber):
        self.userID = phoneNumber
        self.votedSongs = []


    def voteSong(self, songID):
        if myItem in votedSongs:
            self.votedSongs.append(songID)
            return 1
        else:
            return 0

class TextMessage(): 

    """Stores Text Message Data"""


 
