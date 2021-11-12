import pyttsx3
from tweepy import OAuthHandler
import Auth
import tweepy


#setting twitter variable
auth = OAuthHandler(Auth.CONSUMER_KEY, Auth.CONSUMER_SECRET)
auth.set_access_token(Auth.ACCESS_TOKEN, Auth.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


#setting tts

#var declare
engine = pyttsx3.init()
rate = engine.getProperty('rate')

#property setting
engine.setProperty('rate', 150)

#tts say command
def saytext(tptx):
    print(tptx)
    engine.say(tptx)
    engine.runAndWait()
    engine.stop()


stopthread=False