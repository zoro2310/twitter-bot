import gbv

def write_tweet():
    gbv.saytext("Enter text below")
    text=input()
    gbv.api.update_status(text)
    gbv.saytext("Tweeted")