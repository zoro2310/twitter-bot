import gbv
import tweepy


def search_by_tag():
    temptxt="Enter a #tag to continue"
    gbv.saytext(temptxt)
    tag=input()
    tag="#"+tag
    gbv.saytext("Enter number of result you want: ")
    results=int(input())
    tagtimeline=tweepy.Cursor(gbv.api.search,q=tag,count=results,tweet_mode = "extended",lang="en",since="2021-04-04").items()
    for cases, tweet in enumerate(tagtimeline, start=1):
        print(cases,": ")
        print (tweet.created_at, tweet.full_text)
        if cases == results:
            break
        print("\n")

def search_by_user_name():
    gbv.saytext("Enter a user name")
    user_name=input()
    gbv.saytext("Enter number of result you want: ")
    results=input()
    usertimeline = gbv.api.user_timeline(screen_name=user_name,count=results,tweet_mode = "extended")
    for result, i in enumerate(usertimeline, start=1):
        print(result,":")
        print(i.full_text)
        print("\n")