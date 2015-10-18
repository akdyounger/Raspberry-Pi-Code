#I don't need this file anymore since I figured out how to send multiple tweets in one program. This is however, still a good basic tweeting file. 

import sys
import tweepy
import datetime
import time


CONSUMER_KEY = 'hkyM20b8fWBVRplGg5pH1g'
CONSUMER_SECRET = 'KilzlrQDvKNlU8rpvnVA3kBdXoGO6FpzDSHGz8hB21w'
ACCESS_KEY = '1599828776-UDQ4B9PqEmrVKot6LVvNdb4sQ8vFiRe1KSz9bIM'
ACCESS_SECRET = 'RXKFDEdrFgtdlx01v0HQyLqHQAFMvQLlUryCpRqodE'
devicename = "Evanston Pi"
today = datetime.datetime.now()

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

WaterAlertTweet = "%s [%s.%s] @akdyounger Help! My water level is low!" % (devicename, today.minute, today.second)
print WaterAlertTweet


try:
    api.update_status(WaterAlertTweet )
except tweepy.error.TweepError as e :
    print currentTempString
    print "Error from Tweepy:", e