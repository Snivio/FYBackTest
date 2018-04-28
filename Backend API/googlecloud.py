import tweepy
import json
from webob import Response
from textblob import TextBlob
import re
from find_fake import check
import configparser
from flask import jsonify
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
client = language.LanguageServiceClient()
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
    userstream=[]
    # name = request.urlvars['name']
    stuff = api.user_timeline(screen_name = name, count = 500, include_rts = True)
    x=check(name)
    userstream.append({'profileimage':api.get_user(name).profile_image_url.replace("normal","400x400"),'bot_percentage':x})
    
    for status in stuff:
        result = re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", status._json["text"])
    #    document = language.types.sys()
        document = types.language_service_pb2.Document( content=result,type=enums.Document.Type.PLAIN_TEXT)
        annotations = client.analyze_sentiment(document=document)
        score = annotations.document_sentiment.score
        magnitude = annotations.document_sentiment.magnitude
        rating=score*magnitude
        userstream.append({'ts':status.created_at.timestamp(),'text':result,'score':score,'magnitude':magnitude,'rating':rating})

    return jsonify(userstream)
