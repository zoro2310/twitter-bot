#from logging import fatal
import requests
import gbv
import json


dmlist_file="funt/dmlist.txt"
element='DM_LIST'

#COVID API
url = "https://covid-19-tracking.p.rapidapi.com/v1/india"

headers = {
    'x-rapidapi-key': "f8198b5227mshae93178c81a59d3p140b3ajsn78e5a5795fd7",
    'x-rapidapi-host': "covid-19-tracking.p.rapidapi.com"
    }

covidresponse = requests.request("GET", url, headers=headers)

coviddata = covidresponse.json()
status_text="Total Active cases: "+ coviddata['Active Cases_text']+" \n"+"New cases today: "+ coviddata['New Cases_text']+" \n"+"Total recovered: "+ coviddata['Total Recovered_text']



def check_condition(uid):
    with open(dmlist_file, 'r') as json_file:
        data = json.load(json_file)
        for user in data[element]:
            return bool(user['user_id']==uid and user['active'])

def add_dm_user(user_id):
    with open(dmlist_file,'r') as json_file:
        data = json.load(json_file)
        data['DM_LIST'].append({
            'user_id': user_id,
            'active': True
        })
    with open(dmlist_file, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def add_to_dm(tweet):
    check_friend=gbv.api.show_friendship(source_screen_name = tweet.user.screen_name, target_screen_name = "R_TweetBot")
    if check_friend[0].following:
        if check_condition(tweet.user.id_str):
            gbv.api.update_status("@" + tweet.user.screen_name + " Already in DM list", tweet.id)
        else:
            add_dm_user(tweet.user.id_str)
            gbv.api.send_direct_message(tweet.user.id_str, "INSTRUCTIONS: \nSend covidstatus - recive the covid details \nSend covidsos [location] [requirement]- get covid sos tweet based on your location \nSend stop - stop getting messages")
            gbv.api.update_status("@" + tweet.user.screen_name + " Added to DM list", tweet.id)
    else:
        gbv.api.update_status("@" + tweet.user.screen_name + " Please follow to use this", tweet.id)

def remove_from_dm(user_id):
    with open(dmlist_file, 'r') as json_file:
        data = json.load(json_file)
        for i, user in enumerate(data['DM_LIST']):
            if str(user_id) == str(user['user_id']):
                data['DM_LIST'][i]['active'] = False
                with open(dmlist_file, 'w') as json_file:
                    json_file.write(json.dumps(data, indent=4))

def set_active_user(user_id):
    with open(dmlist_file, 'r') as json_file:
        data = json.load(json_file)
        for i, user in enumerate(data['DM_LIST']):
            if str(user_id) == str(user['user_id']):
                data['DM_LIST'][i]['active'] = True
                with open(dmlist_file, 'w') as json_file:
                    json_file.write(json.dumps(data, indent=4))



def covid_data():
    gbv.saytext("Total Active cases: "+ coviddata['Active Cases_text'])
    gbv.saytext("New cases today: "+ coviddata['New Cases_text'])
    gbv.saytext("Total recovered: "+ coviddata['Total Recovered_text'])



def coviddmfunt():  # sourcery no-metrics
    messages = gbv.api.list_direct_messages(count=5)
    for message in messages:
        sender_id = message.message_create["sender_id"]
        if sender_id!='1378697655744745481':
            with open(dmlist_file) as json_file:
                data = json.load(json_file)
                for user in data[element]:
                    text = message.message_create["message_data"]["text"]
                    if str(user['user_id'])==sender_id and user['active'] and sender_id!='1378697655744745481':
                            if text=='covidstatus':
                                gbv.api.send_direct_message(sender_id, status_text)
                            if text=='stop':
                                remove_from_dm(sender_id)
                                gbv.api.send_direct_message(sender_id, "stopped \nSend start to start again")
                            if 'covidsos' in text:
                                temp_text=text.split()
                                link_s="https://twitter.com/search?q=%23covidsos%20"+temp_text[1]+"%20"+temp_text[2]+"%20available"
                                gbv.api.send_direct_message(sender_id, link_s)
                            if text=='start':
                                gbv.api.send_direct_message(sender_id, "Already enabled")

                    else:
                        if text=='start':
                            set_active_user(sender_id)
                            gbv.api.send_direct_message(sender_id, "INSTRUCTIONS: \nSend covidstatus - recive the covid details \nSend covidsos [location] [requirement]- get covid sos tweet based on your location \nSend stop - stop getting messages")
                        continue
        else:
            break

def search_sos():
    gbv.saytext("Enter location and requirment")
    req=input()
    gbv.saytext("Enter number of result you want: ")
    noq=input()
    sos_result=gbv.api.search(q=req,count=noq,tweet_mode = "extended",hashtag="#coronasos")
    for result,i in enumerate(sos_result,start=1):
        print(result,":")
        #srn=gbv.api.get_user(i.user.id)
        #print(i.id)
        print(i.created_at)
        print("text:"+i.full_text)
        print("LINK: https://twitter.com/R_TweetBot/status/"+i.id_str)
        print("\n")