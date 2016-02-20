from flask import Flask, request, redirect
from gmusicapi import Mobileclient
import twilio.twiml
import classes

api = Mobileclient()
#implement a solution to have user login
logged_in = api.login('jusanden7@gmail.com', 'zpewalrdeytbdhmu')
if !logged_in:
    print("Log in failed, please verify login details")
else: 
    print("logged in")

def playsong(songID):
def parseQuery(query):
    results = Mobileclient.search_all_access(query, 20)
    parsedID = results['song_hits'][1]['track']['storeID']
    parsedTitle = results['song_hits'][1]['track']['title']
    return Song(parsedTitle, parsedID)



if __name__ = "__main__":
    textjam()

