import gbv
from funt import covidsos


greetings = ['hi', 'hello', 'hey']

lastseen_file='funt/lastseen.txt'
unchecked_file = 'funt/unchecked.txt'


def check_mentions():
    with open(lastseen_file, 'r') as file_read:
        lastseen_id = int(file_read.read().strip())
    if lastseen_id != 00:
        tweets = gbv.api.mentions_timeline(lastseen_id, tweet_mode='extended')
    else:
        tweets = gbv.api.mentions_timeline(tweet_mode='extended')
    
    for tweet in reversed(tweets): 
        flag=True
        if '#like' in tweet.full_text.lower():
            gbv.api.create_favorite(tweet.id)
            flag=False
        if '#reply' in tweet.full_text.lower():
            gbv.api.update_status("@" + tweet.user.screen_name + " This is an Auto Generated Reply from TweetBot", tweet.id)
            flag=False
        if '#coviddm' in tweet.full_text.lower() and 'start' in tweet.full_text.lower():
            covidsos.add_to_dm(tweet)
            flag=False
        if any(x in tweet.full_text.lower() for x in greetings):
            gbv.api.update_status("@" + tweet.user.screen_name + " Hey!", tweet.id)
            flag=False
        if flag:
            with open(unchecked_file, 'a') as file_write:
                file_write.write(str(tweet.id)+"\n")
        with open(lastseen_file, 'w') as file_write:
            file_write.write(str(lastseen_id))


def checkunreplied():
    def updatefile(uncheck_file, tweet):
        with open(unchecked_file, "w") as f:
            for line in uncheck_file:
                if line.strip("\n") != str(tweet.id):
                    f.write(line)
    
    uncheck_file = open(unchecked_file, 'r+')
    for line in uncheck_file:
        tweet = gbv.api.get_status(line)
        gbv.saytext(tweet.user.screen_name +" "+ tweet.text)
        gbv.saytext("What do you want to do? [reply or leave]")
        reply_input=input()
        if reply_input== 'reply':
            gbv.saytext("Enter text below: ")
            reply_text=input()
            gbv.api.update_status("@" + tweet.user.screen_name +" "+ reply_text, tweet.id)
            updatefile(uncheck_file, tweet)
        else:
            updatefile(uncheck_file, tweet)
            continue

