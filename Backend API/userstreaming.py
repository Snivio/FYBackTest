
import tweepy
import json
from webob import Response
from textblob import TextBlob
import re
from find_fake import check
import configparser
from flask import jsonify
config = configparser.ConfigParser()
config.read('config.ini')

ckey = config['TWITTER']['ckey']
csecret = config['TWITTER']['csecret']
atoken =  config['TWITTER']['atoken']
asecret =  config['TWITTER']['asecret']



auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)
def post_view(name):
    cn=0
    userstream=[]
    # name = request.urlvars['name']
    stuff = api.user_timeline(screen_name = name, count = 100, include_rts = True)
    x=check(name)
    userstream.append({'profileimage':api.get_user(name).profile_image_url.replace("normal","400x400"),'bot_percentage':x})
    
    for status in stuff:
        result = re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", status._json["text"])
        analysis = TextBlob(result)
        #print (status)
        cn=cn+1
        userstream.append({'postNumber':cn,'ts':status.created_at.timestamp(),'post':result,'polarity':analysis.sentiment.polarity})

    return jsonify(userstream)


