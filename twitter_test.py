#!/usr/bin/env python
# -*- coding:utf-8 -*-

#    # installation
#    $ pip install requests requests_oauthlib
#
#    $ python twitter_test.py "検索したい単語"
#


from requests_oauthlib import OAuth1Session
import json
import sys

oath_key_dict = {
    "consumer_key": "****",
    "consumer_secret": "****",
    "access_token": "****",
    "access_token_secret": "****"
}

max_count = 1000

# 使わない、参考に
'''
def main(word):
    tweets = tweet_search(word, oath_key_dict)
    print(len(tweets["statuses"]))
    for tweet in tweets["statuses"]:
        tweet_id = tweet[u'id_str']
        text = tweet[u'text']
        created_at = tweet[u'created_at']
        user_id = tweet[u'user'][u'id_str']
        user_description = tweet[u'user'][u'description']
        screen_name = tweet[u'user'][u'screen_name']
        user_name = tweet[u'user'][u'name']
        print("tweet_id:", tweet_id)
        #print("text:", text)
        #print("created_at:", created_at)
        #print("user_id:", user_id)
        #print("user_desc:", user_description)
        #print("screen_name:", screen_name)
        #print("user_name:", user_name)
    return tweets
'''

def get_text(word):
    text_list = []
    max_id = 0
    #for _ in range(max_count//100):
    while True:
        tweets = tweet_search(word, oath_key_dict, max_id)
        i = 0
        for tweet in tweets["statuses"]:
            text_list.append(tweet[u'text'])
            i += 1
            if i == 100:
                max_id = int(tweet[u'id_str'])-1
        print(len(set(text_list)))
        if len(set(text_list)) >= max_count:
            break
    # 重複や空を削除
    text_list = list(set(text_list))
    text_list = text_list[:max_count]
    print(len(text_list))
    return text_list


def create_oath_session(oath_key_dict):
    oath = OAuth1Session(
        oath_key_dict["consumer_key"],
        oath_key_dict["consumer_secret"],
        oath_key_dict["access_token"],
        oath_key_dict["access_token_secret"]
    )
    return oath

def tweet_search(search_word, oath_key_dict, max_id=0):
    url = "https://api.twitter.com/1.1/search/tweets.json?"
    params = {
        "q": search_word,
        "lang": "ja",
        "result_type": "recent",
        "count": "100",
        "max_id": max_id
    }
    oath = create_oath_session(oath_key_dict)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print("Error code: %d" %(responce.status_code))
        return None
    tweets = json.loads(responce.text)
    return tweets

if __name__ == "__main__":
    #main(sys.argv[1])
    get_text(sys.argv[1])