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
import MeCab

import urllib
from urllib import request, parse

oath_key_dict = {
    "consumer_key": config.consumer_key,
    "consumer_secret": config.consumer_secret,
    "access_token": config.access_token,
    "access_token_secret": config.access_token_secret
}

max_count = 300




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
def pn_info():
    f = open("pn_ja.txt",encoding="shift-jis")
    line = f.readline()
    pn_info = [[],[],[],[],[]]
    hinshi = ['形容詞', '動詞', '名詞', '副詞', '助動詞']
    while line:
        word_info = line.replace('\n','').split(":")
        for i in range(5):
            if word_info[2] == hinshi[i]:
                word_info.pop(2)
                pn_info[i].append(word_info)
        line = f.readline()
    return pn_info

#　ストップワードのlistを返す
def stop_word():
    f = open("Slothlib.txt")
    lines = f.read()
    return lines.split()


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

pn_info = pn_info()
hinshi = ['形容詞', '動詞', '名詞', '副詞', '助動詞']
stops = stop_word()

def texts_pn(texts, word):
    m = MeCab.Tagger()
    pn_list = []
    relate = {}
    for i,text in enumerate(texts):
        sys.stdout.write("\r感情分析中... %d" % (i+1))
        sys.stdout.flush()
        pn = 0
        for chunk in m.parse(text).splitlines()[:-1]:
            #(surface, feature) = chunk.split('\t')
            if len(chunk.split('\t')) != 2:
                continue
            feature = chunk.split('\t')[1]
            feature = feature.split(",")

            #関連単語カウント
            if feature[0] in hinshi[0:3] and (not feature[1] in ["非自立","接尾","特殊","代名詞"]):
                if feature[-3] in relate.keys():
                    relate[feature[-3]] += 1
                elif (not feature[-3] in stops) and feature[-3] != word:
                    relate[feature[-3]] = 1


            for i in range(5):
                if feature[0]==hinshi[i]:
                    for info in pn_info[i]:
                        # feature[-3]　は　原型, そのままなら surface
                        if (feature[-3] == info[0] or feature[-3] == info[1]) and abs(float(info[2]))>0.9 :

                            pn += float(info[2])
                            #if i < 3 :
                             #   if feature[-3] in relate.keys():
                              #      relate[feature[-3]] += 1
                               # elif (not feature[-3] in stops) and feature[-3] != word:
                                #    relate[feature[-3]] = 1

                            break
        pn_list.append(pn)
    return pn_list, relate

def main(word):
    texts = get_text(word)
    pn_list, relate = texts_pn(texts, word)
    print(len(relate))
    #print(max([(v,k) for k,v in relate.items()]))

    sorted_list = sorted(relate.items(), key=lambda x:x[1], reverse=True)
    print(sorted_list[:10])
    i=0
    freq = []
    #while i < 5:
    #    k,v = sorted_dic.next
    #    freq.append([k,v])
    #    i += 1
    #print(freq)
    p_n_neu = [0,0,0]
    for pn in pn_list:
        if pn > 0:
            p_n_neu[0] += 1
        elif pn < 0:
            p_n_neu[2] += 1
        else:
            p_n_neu[1] += 1
    print (p_n_neu)
    #return texts, pn_list
    return p_n_neu, sorted_list[:10]

#感情分析API、使えない。。。
'''
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
'''

if __name__ == "__main__":
    print(main(sys.argv[1]))
