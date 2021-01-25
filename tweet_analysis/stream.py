import got3 as got,  requests as req
import time, datetime, re, csv, traceback
from convinience_method import my_print, sub_text
#twitter_apiを使うために必要
import rest_Api, requests_oauthlib_module
api  = rest_Api.api
auth = requests_oauthlib_module.auth
#ここまで


keyword        = input("検索ワードを指定してください\n")
since_date_str = input("開始日を指定してください(「YYYY-mm-dd形式で入力してください」)\n")
until_date_str = input("終了日を指定してください(「YYYY-mm-dd形式で入力してください」)\n")
dt = datetime.datetime.now()
file_text = []
wf     = open(keyword+"_"+since_date_str+"to"+until_date_str+".csv", "w", encoding="utf_8")
writer = csv.writer(wf, lineterminator="\n")

if not re.match(r"\d{4}-\d{2}-\d{2}", until_date_str):
    until_date_str = dt.strftime("%Y-%m-%d")
if not re.match(r"\d{4}-\d{2}-\d{2}", since_date_str):
    since_date_str = (dt - datetime.timedelta(weeks=1)).strftime("%Y-%m-%d")
#時分秒を追加
if until_date_str == datetime.datetime.strftime(dt, "%Y-%m-%d"):
    until_date_str1 = until_date_str+"_"+str(dt.hour)+":00:00"
else:
    until_date_str1 = until_date_str+"_23:59:59"
since_date_str1     = since_date_str+"_00:00:00"


until_date_next = (datetime.datetime.strptime(until_date_str1, "%Y-%m-%d_%H:%M:%S") - datetime.timedelta(minutes =1)).strftime("%Y-%m-%d_%H:%M:%S")
until_date_from = (datetime.datetime.strptime(until_date_str1, "%Y-%m-%d_%H:%M:%S") - datetime.timedelta(minutes =2)).strftime("%Y-%m-%d_%H:%M:%S")
#since_date_next = (datetime.datetime.strptime(since_date_str, "%Y-%m-%d")- datetime.timedelta(hours=1)).strftime("%Y-%m-%d")
print("start："+until_date_str1)
print("next："+until_date_next)

try:
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword).setSince(until_date_next+"_JST").setUntil(
            until_date_str1+"_JST")

    for tweet in got.manager.TweetManager.getTweets(tweetCriteria):
        replace_text = re.sub(tweet.permalink, "", tweet.text)
        replace_text = sub_text(replace_text)
        file_text.append([0, str(tweet.date), "'"+tweet.id+"'", tweet.username, tweet.retweets, tweet.favorites, replace_text, tweet.permalink, tweet.urls])
        
    writer.writerow(["label", "created", "id", "name", "RT", "fav", "text", "tweet_url", "quote_url"])
    writer.writerows(file_text)
    wf.close()
    time.sleep(30)
    print("よーし")
    file_text.clear()
except:
    writer.writerow(["label", "created", "id", "name", "RT", "fav", "text", "url"])
    writer.writerows(file_text)
    wf.close()
    file_text.clear()
    time.sleep(30)
    print(traceback.format_exc())
    
while (datetime.datetime.strptime(until_date_next, "%Y-%m-%d_%H:%M:%S") - datetime.datetime.strptime(since_date_str1, "%Y-%m-%d_%H:%M:%S")).total_seconds() > 0:
    print("next："+ until_date_next)
    print("from："+ until_date_from)
    #time.sleep(30)
    try:
        wf     = open(keyword+"_"+since_date_str+"to"+until_date_str+".csv", "a", encoding="utf_8")
        writer = csv.writer(wf, lineterminator="\n")
        
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(keyword).setSince(until_date_from+"_JST").setUntil(
            until_date_next+"_JST")
        for tweet in got.manager.TweetManager.getTweets(tweetCriteria):
            replace_text = re.sub(tweet.permalink, "", tweet.text)
            replace_text = sub_text(replace_text)
            file_text.append([0, str(tweet.date), "'"+tweet.id+"'", tweet.username, tweet.retweets, tweet.favorites, replace_text, tweet.permalink, tweet.urls])

        writer.writerows(file_text)
        wf.close()
        file_text.clear()
        print("よーし")
        time.sleep(30)

        until_date_from = (datetime.datetime.strptime(until_date_from, "%Y-%m-%d_%H:%M:%S") - datetime.timedelta(minutes =1)).strftime("%Y-%m-%d_%H:%M:%S")
        until_date_next = (datetime.datetime.strptime(until_date_next, "%Y-%m-%d_%H:%M:%S") - datetime.timedelta(minutes =1)).strftime("%Y-%m-%d_%H:%M:%S")
        
    except:
        writer.writerows(file_text)
        wf.close()
        file_text.clear()
        print(traceback.format_exc())
        time.sleep(30)
        until_date_from = (datetime.datetime.strptime(until_date_from, "%Y-%m-%d_%H:%M:%S") - datetime.timedelta(minutes =1)).strftime("%Y-%m-%d_%H:%M:%S")
        until_date_next = (datetime.datetime.strptime(until_date_next, "%Y-%m-%d_%H:%M:%S") - datetime.timedelta(minutes =1)).strftime("%Y-%m-%d_%H:%M:%S")
        continue

