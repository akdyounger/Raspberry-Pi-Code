import sys
import tweepy

CONSUMER_KEY = 'hkyM20b8fWBVRplGg5pH1g'
CONSUMER_SECRET = 'KilzlrQDvKNlU8rpvnVA3kBdXoGO6FpzDSHGz8hB21w'
ACCESS_KEY = '1599828776-UDQ4B9PqEmrVKot6LVvNdb4sQ8vFiRe1KSz9bIM'
ACCESS_SECRET = 'RXKFDEdrFgtdlx01v0HQyLqHQAFMvQLlUryCpRqodE'

WhatToTweet = (sys.argv[1])


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
api.update_status(status=WhatToTweet)

