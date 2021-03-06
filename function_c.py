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
import multiprocessing as mp
import time
import stalker as st
import re

import urllib
from urllib import request, parse

oath_key_dict = {
    "consumer_key": config.consumer_key,
    "consumer_secret": config.consumer_secret,
    "access_token": config.access_token,
    "access_token_secret": config.access_token_secret
}

max_count = 200
num_process = 2




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

def get_text_all():
    text_list = []
    max_id = 0
    #for _ in range(max_count//100):
    while True:
        tweets = tweet_search_all(oath_key_dict, max_id)
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

def tweet_search_all(oath_key_dict, max_id=0):
    url = "https://api.twitter.com/1.1/search/tweets.json?"
    params = {
        "q": "*",
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
        text = text.replace("#","")
        text = re.sub(r'[a-z]+', "", text)
        #print(text)
        for chunk in m.parse(text).splitlines()[:-1]:
            #(surface, feature) = chunk.split('\t')
            if len(chunk.split('\t')) != 2:
                continue
            feature = chunk.split('\t')[1]
            feature = feature.split(",")

            # 関連単語カウント
            if feature[0] in hinshi[0:3] and (not feature[1] in ["非自立","接尾","特殊","代名詞"]):
                if feature[-3] in relate.keys():
                    relate[feature[-3]] += 1
                elif (not feature[-3] in stops) and feature[-3] != word:
                    relate[feature[-3]] = 1

            # ポジネガ数値計算
            for i in range(5):
                if feature[0]==hinshi[i]:
                    for info in pn_info[i]:
                        # feature[-3]　は　原型, そのままなら surface
                        if (feature[-3] == info[0] or feature[-3] == info[1]) and abs(float(info[2]))>0.9:
                            pn += float(info[2])
                            break
        pn_list.append(pn)
    return pn_list, relate

def texts_pn_all(texts):
    m = MeCab.Tagger()
    pn_list = []
    for i,text in enumerate(texts):
        sys.stdout.write("\r感情分析中... %d" % (i+1))
        sys.stdout.flush()
        pn = 0
        text = text.replace("#","")
        text = re.sub(r'[a-z]+', "", text)
        for chunk in m.parse(text).splitlines()[:-1]:
            #(surface, feature) = chunk.split('\t')
            if len(chunk.split('\t')) != 2:
                continue
            feature = chunk.split('\t')[1]
            feature = feature.split(",")


            # ポジネガ数値計算
            for i in range(5):
                if feature[0]==hinshi[i]:
                    for info in pn_info[i]:
                        # feature[-3]　は　原型, そのままなら surface
                        if (feature[-3] == info[0] or feature[-3] == info[1]) and abs(float(info[2]))>0.9:
                            pn += float(info[2])
                            break
        pn_list.append(pn)
    return pn_list

def wrap_texts_pn(texts_word):
    return texts_pn(*texts_word)

def split_array(ar, n_group):
    splited = []
    for i_chunk in range(n_group):
        splited.append(ar[i_chunk * len(ar) // n_group:(i_chunk + 1) * len(ar) // n_group])
    return splited

def main(word):
    start = time.time()
    texts = get_text(word)
    #pn_list, relate = texts_pn(texts, word)
    #print(texts)

    split_text = split_array(texts,num_process)
    print(len(split_text),"プロセス")

    pool = mp.Pool(num_process)
    args = [(i, word) for i in split_text]
    callbacks = pool.map(wrap_texts_pn, args)
    pn_list = []
    relate = {}
    for callback in callbacks:
        pn_list = pn_list + callback[0]
        relate.update(callback[1])
    sorted_list = sorted(relate.items(), key=lambda x:x[1], reverse=True)
    print("\n",sorted_list[:10])

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
    print(time.time() - start)
    return p_n_neu, sorted_list[:10]

def main_all():
    start = time.time()
    texts = get_text_all()
    #pn_list, relate = texts_pn(texts, word)
    #print(texts)

    split_text = split_array(texts,num_process)
    print(len(split_text),"プロセス")

    pool = mp.Pool(num_process)
    #args = [(i, word) for i in split_text]
    callbacks = pool.map(texts_pn_all, split_text)
    pn_list = []
    for callback in callbacks:
        pn_list = pn_list + callback

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
    print(time.time() - start)
    return p_n_neu

def insta(word):
    start = time.time()
    texts = st.instagram(word,max_count)
    texts = texts[:max_count]
    split_text = split_array(texts,num_process)
    print(len(split_text),"プロセス")

    pool = mp.Pool(num_process)
    args = [(i, word) for i in split_text]
    callbacks = pool.map(wrap_texts_pn, args)
    pn_list = []
    relate = {}
    for callback in callbacks:
        pn_list = pn_list + callback[0]
        relate.update(callback[1])
    sorted_list = sorted(relate.items(), key=lambda x:x[1], reverse=True)
    print("\n",sorted_list[:10])

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
    print(time.time() - start)
    return p_n_neu, sorted_list[:10]

def insta_all(texts):
    start = time.time()
    #pn_list, relate = texts_pn(texts, word)
    #print(texts)

    split_text = split_array(texts,num_process)
    print(len(split_text),"プロセス")

    pool = mp.Pool(num_process)
    #args = [(i, word) for i in split_text]
    callbacks = pool.map(texts_pn_all, split_text)
    pn_list = []
    for callback in callbacks:
        pn_list = pn_list + callback

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
    print(time.time() - start)
    return p_n_neu



if __name__ == "__main__":
    #main_all()
    print("Twitter\n",main(sys.argv[1]))
    print("Instagram\n",insta(sys.argv[1]))

