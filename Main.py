from funt.covidsos import covid_data, search_sos
from funt.searchtweet import search_by_tag, search_by_user_name
from funt.checkmentions import checkunreplied
from funt.writetweet import write_tweet
import gbv
from funt.background_task import start_scan, stop_scan, t1


    
gbv.saytext("Hello")
gbv.saytext("Starting DM Scan and Tweet Scan in background")
t1.start()


while True:
    
    print("\n\nTweet Bot Menu")
    print("1. Make a tweet")
    print("2. Check for unreplied tweets")
    print("3. Covid Status")
    print("4. Search tweet by tag")
    print("5. Search tweet by user name")
    print("6. Search for coronasos")
    print("7. Stop background scans")
    print("8. Start background scans")
    print("9. Exit Tweet Bot")

    print("Enter your choice:")
    choise=int(input())
    print("\n")

    if choise == 1:
        write_tweet()
    elif choise == 2:
        checkunreplied()
    elif choise == 3:
        covid_data()
    elif choise == 4:
        search_by_tag()
    elif choise == 5:
        search_by_user_name()
    elif choise == 6:
        search_sos()
    elif choise == 7:
        stop_scan()
    elif choise == 8:
        start_scan()
    else:
        stopthread=True
        stop_scan()
        gbv.saytext("Good bye")
        break