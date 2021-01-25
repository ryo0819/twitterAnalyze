import tweepy

#REST APIを使う際に必要となるもの
#自身でtwitterのアクセストークン等を取得する必要あり
consumer_key = 'xxxxxxxxxxxxxxxx'
consumer_secret = 'xxxxxxxxxxxxxxxx'
access_token = 'xxxxxxxxxxxxxxxx'
access_token_secret = 'xxxxxxxxxxxxxxxx'

#認証
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
