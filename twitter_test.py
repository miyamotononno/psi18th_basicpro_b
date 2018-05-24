#!/usr/bin/env python
# -*- coding:utf-8 -*-

#    # installation
#    $ pip install requests requests_oauthlib
#
#    $ python twitter_test.py 検索したい単語
#


from requests_oauthlib import OAuth1Session
import json
import sys
import config

import urllib
from urllib import request, parse

oath_key_dict = {
    "consumer_key": config.consumer_key,
    "consumer_secret": config.consumer_secret,
    "access_token": config.access_token,
    "access_token_secret": config.access_token_secret
}

max_count = 200

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
        for i,tweet in enumerate(tweets["statuses"]):
            text_list.append(tweet[u'text'])
            if i == 99:
                max_id = int(tweet[u'id_str'])-1
        sys.stdout.write("\rTweet取得中... %d" % len(set(text_list)))
        sys.stdout.flush()
        if len(set(text_list)) >= max_count or not len(tweets["statuses"])==100:
            break
    # 重複や空を削除
    text_list = list(set(text_list))
    text_list = text_list[:max_count]
    print("\n取得数",len(text_list))
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

def posi_or_nega(text):
    # 基本URI
    url = 'http://ap.mextractr.net/ma9/emotion_analyzer?'

    # URIパラメータのデータ
    # appkeyは個々人で取得してください
    param = {
        'out': 'json',
        'apikey': '8D0342623B1801F4E3262E2166E70BB8AA269E5A',
        'text': text
    }

    # URIパラメータの文字列の作成
    #  Getリクエストの形式に整形  (text=アクセスが拒否されました。がっかり。&out=json&appley=8D0342623B1801F4E3262E2166E70BB8AA269E5A)
    paramStr = urllib.parse.urlencode(param)

    # 読み込むオブジェクトの作成
    readObj = urllib.request.urlopen(url + paramStr)

    # webAPIからのJSONを取得
    res = readObj.read().decode()
    #print(res)
    # webAPIから取得したJSONデータをpythonで使える形に変換する
    data = json.loads(res)

    posi_or_nega = data['likedislike'] + data['joysad'] - abs(data['angerfear'])

    return posi_or_nega


def main(word):
    texts = get_text(word)
    emotion = []
    for text in texts:
        p_n = posi_or_nega(text)
        emotion.append(p_n)
        sys.stdout.write("\r感情分析中... %d" % len(emotion))
        sys.stdout.flush()
    posi_nega_neutral = [0,0,0]
    for i in emotion:
        if i >0:
            posi_nega_neutral[0] += 1
        elif i<0:
            posi_nega_neutral[1] += 1
        else:
            posi_nega_neutral[2] += 1
    return posi_nega_neutral

if __name__ == "__main__":
    print(main(sys.argv[1]))