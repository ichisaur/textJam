from flask import Flask, request, redirect
from gmusicapi import Mobileclient
import twilio.twiml
import classes



api = Mobileclient()
#implement a solution to have user login
logged_in = api.login('jusanden7@gmail.com', 'zpewalrdeytbdhmu', Mobileclient.FROM_MAC_ADDRESS)
if (logged_in):
    print("logged in")
else:
    print("Log in failed, please verify login details")

    

def parseQuery(query):
    results = api.search_all_access(query, 10)
    parsedID = results['song_hits'][0]['track']['storeId']
    parsedTitle = results['song_hits'][0]['track']['title']
    return classes.Song(parsedTitle, parsedID)


s = parseQuery('Yellow')
print(s.title)







