from requests_oauthlib import OAuth1

#自身でtwitterのアクセストークン等を取得する必要あり
consumer_key = 'xxxxxxxxxxxxxxxx'
consumer_secret = 'xxxxxxxxxxxxxxxx'
access_token = 'xxxxxxxxxxxxxxxx'
access_token_secret = 'xxxxxxxxxxxxxxxx'

auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)
