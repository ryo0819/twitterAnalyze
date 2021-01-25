import pathlib, glob,re, sys, os
from gensim.models import word2vec
import MeCab, matplotlib.pyplot as plt, matplotlib as mpl
import numpy as np, pandas as pd
import nakamura
from convinience_method import my_print, sub_text
sentiments = nakamura.sentiments

model = word2vec.Word2Vec.load("wiki.model")
mt    = MeCab.Tagger(r"C:\progra~1\MeCab\etc\mecabrc")
mt.parse("")

file_name = "桜を見る会_2019-11-01to2019-11-30"
df        = pd.read_csv(file_name+".csv", encoding="utf_8")
try:
    keyword = file_name.split("_")[0]
except:
    pass

try:
    keyword = file_name.split("_")[6]
except:
    pass

node       = mt.parseToNode(keyword)
node_count = 0
#key_w = []#表記ゆれに使おう
while node:
    if node.feature.startswith("BOS/EOS"):
        node = node.next
        continue
    node_count += 1
    #key_w.append(node.feature.split(",")[6])
    node = node.next
print(keyword+"："+str(node_count))
#input(key_w)

date_time_list = []#日付_時間
date_list        = []#日付
text_date_dict = {}#日付をキーとしたテキスト

for row in df.itertuples():
    try:
        i = row.created.split(" ")[0] +"_" + row.created.split(" ")[1].split(":")[0]
    except:
        continue
    if i in date_time_list:
        text_date_dict[i].append(row.text)
        continue
    if re.match(r"^\d{4}\/\d{2}\/\d{2}", i):
        text_date_dict[i] = [row.text]
        date_time_list.append(i)
        if not row.created.split(" ")[0] in date_list:
            date_list.append(row.created.split(" ")[0])
    elif re.match(r"^\d{4}-\d{2}-\d{2}", i):
        text_date_dict[i] = [row.text]
        date_time_list.append(i)
        if not row.created.split(" ")[0] in date_list:
            date_list.append(row.created.split(" ")[0])
            
        
date_time_list   = sorted(date_time_list, reverse = False)
date_list        = sorted(date_list, reverse = False)

noun             = {}#名詞
noun_h           = {}#人名
verb             = {}#動詞（自立）
tweet_time_count = {}#時間ごとのテキスト

for i in date_time_list:
    noun[i]             = {}
    noun_h[i]           = {}
    verb[i]             = {}
    tweet_time_count[i] = len(text_date_dict[i])

    """for line in text_date_dict[i]:
        line = sub_text(str(line))
        if node_count > 1:
            if keyword in line:
                line = line.replace("スタバの福袋", keyword)#要修正
                if not keyword in noun[i].keys():
                    noun[i][keyword]  = 1
                else:
                    noun[i][keyword] += 1
                
            text_splited = line.split(keyword)
            
            for l in text_splited:
                node = mt.parseToNode(l)
                while node:
                    fields = node.feature.split(",")#品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
                    node = node.next
                    
                    if fields[6] == "*":
                        continue
                    if fields[0] == '動詞'  and fields[1] == "自立":
                        if not fields[6] in verb[i].keys():
                            verb[i][fields[6]]  = 1
                        else:
                            verb[i][fields[6]] += 1
                    if (fields[1] == "アルファベット" and len(fields[6]) == 1) or fields[6]== "???"or fields[6] == "()":
                        continue
                    if fields[1] == '固有名詞':
                        if fields[2] == "人名":
                            if not fields[6] in noun_h[i].keys():
                                noun_h[i][fields[6]]  = 1
                            else:
                                noun_h[i][fields[6]] += 1
                        elif not fields[6] in noun[i].keys():
                            noun[i][fields[6]]  = 1
                        else:
                            noun[i][fields[6]] += 1
        else:
            text_splited = line.split(keyword)
            for l in text_splited:
                node = mt.parseToNode(l)
                while node:
                    fields = node.feature.split(",")#品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
                    node = node.next
                    
                    if fields[6] == "*":
                        continue
                    if fields[0] == '動詞'  and fields[1] == "自立":
                        if not fields[6] in verb[i].keys():
                            verb[i][fields[6]]  = 1
                        else:
                            verb[i][fields[6]] += 1
                    if (fields[1] == "アルファベット" and len(fields[6]) == 1) or fields[6]== "???"or fields[6] == "()":
                        continue
                    if fields[1] == '固有名詞':
                        if fields[2] == "人名":
                            if not fields[6] in noun_h[i].keys():
                                noun_h[i][fields[6]]  = 1
                            else:
                                noun_h[i][fields[6]] += 1
                        elif not fields[6] in noun[i].keys():
                            noun[i][fields[6]]  = 1
                        else:
                            noun[i][fields[6]] += 1

                    #ここで判断するのではなくて表記ゆれを訂正してからのほうがよい
print("名詞動詞の収集完了")
"""
#ikitinashiを再現するにはここをコメントアウト
#ikitiariにするにはコメントアウトを外す
"""#次なる目標→話題と原因
noun_and_verb = {}
copy_noun     = {}#元の名詞群
copy_verb     = {}#元の動詞群
with open("sample2.txt", "w", encoding="utf_8") as rf:
    for date in date_time_list:
        noun_and_verb[date] = []
        copy_noun[date] = noun[date].copy()
        
        [noun[date].pop(n[0]) for n in list(noun[date].items()) if n[1] < 1000]
        [verb[date].pop(v[0]) for v in list(verb[date].items()) if v[1] < 100]
        
        rf.write(date+"\n")
        for n in noun[date].items():
            for v in verb[date].items():
                noun_and_verb[date].append([n[0], v[0]])
        rf.write(str(noun_and_verb[date])+"\n")
print("選別完了")
"""

#日ごとのツイート数
tweet_sum = {}
for date in date_list:
    sum_t = 0
    for time in date_time_list:
        if re.match(date, time):
            sum_t += tweet_time_count[time]
    tweet_sum[date] = sum_t

print("---ピーク状況---")
#時間幅で決めるか
#ピークから何割以上がどれだけ続くか
#の２択
peak_t = [i for i in tweet_time_count.values()]#時間
peak_d = [i for i in tweet_sum.values()]#日にち

peak_time_l = []
peak_time_r = []
left = reversed(date_time_list[:peak_t.index(max(peak_t))])
right = date_time_list[peak_t.index(max(peak_t)):]

for date in left:
    if tweet_time_count[date]>(max(peak_t)*0.4):
        peak_time_l.append(date)
    else:
        break
if not peak_time_l:
    peak_time_l.append(date_time_list[peak_t.index(max(peak_t))-1])
peak_time_l.reverse()
for date in right:
    if tweet_time_count[date]>(max(peak_t)*0.4):
        peak_time_r.append(date)
    else:
        break

peak_time = peak_time_l + peak_time_r


#print("ピーク(日)のタイミング："+str(peak_day_list))
#print("最もピーク(日)のタイミング："+date_list[peak_day.index(max(peak_day))])
print("ピーク(時間)のタイミング："+str(peak_time))
print("最もピーク(時間)のタイミング："+date_time_list[peak_t.index(max(peak_t))])


phrase_dict = {}#日ごとの感情語を含むテキストを「日付辞書→テキストリスト」の形式
senti_words = {}#日ごとの感情語の出現回数を「日付辞書→ネガポジ辞書→単語辞書」の形式
#noun_and_verb_date = []#未定
topn_three = {}#その日の感情語トップ３
topp_three = {}
#neg_pos  =  {}#ネガポジを分ける「日付辞書→ネガポジ辞書→単語辞書」の形式、senti_wordsを使わない場合はこっち
nakamura_sentiments = {0:"哀",1:"恥",2:"怒",3:"嫌",4:"怖",5:"驚",6:"昂", 7:"好",8:"安",9:"喜"}#感情の分類
         
            
for i in peak_time:
    #"""if not noun_and_verb[i]:
    #   print(i+"に名詞動詞群はありません")
    #  continue
    #noun_and_verb_date.append(i)"""
    senti_words[i] = {"n":{}, "p":{}}
    phrase_dict[i] = {}

    for line in text_date_dict[i]:
        if re.search(keyword, str(line)):
            line = sub_text(str(line))
            text_splited = line.split(keyword)
            for l in text_splited:
                node = mt.parseToNode(l)
                while node:
                    fields = node.feature.split(",")#品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
                    node = node.next

                    if  fields[0] == "形容詞" or "形容詞" in fields[1] or fields[0] == '動詞' or fields[0] == '名詞':
                        if not fields[6] in phrase_dict[i].keys():
                            phrase_dict[i][fields[6]] = [line]
                            for n, sentiment in enumerate(sentiments):
                                if fields[6] in sentiment:
                                    if 0 <= n <= 6:
                                        senti_words[i]["n"][fields[6]]  = 1
                                    elif 7 <= n <= 9:
                                        senti_words[i]["p"][fields[6]]  = 1
                                    break
                        else:
                            phrase_dict[i][fields[6]].append(line)
                            for n, sentiment in enumerate(sentiments):
                                if fields[6] in sentiment:
                                        if 0 <= n <= 6:
                                            senti_words[i]["n"][fields[6]]  += 1
                                        elif 7 <= n <= 9:
                                            senti_words[i]["p"][fields[6]]  += 1
                                        break
                                
    #感情語を降順に並べ替え
    senti_words[i]["n"] = dict(sorted(senti_words[i]["n"].items(), key=lambda x: x[1], reverse = True)[:3])
    senti_words[i]["p"] = dict(sorted(senti_words[i]["p"].items(), key=lambda x: x[1], reverse = True)[:3])
    """print(senti_words[i])
    print(sum(senti_words[i]["n"].values()))
    print(sum(senti_words[i]["p"].values()))
    input()"""
print("感情語を抽出完了")



sum_n = 0
sum_p = 0
with open("sentil.txt", "w", encoding="utf_8") as rf:
    for date in peak_time_l:
        #sum_n += sum(senti_words[date]["n"].values())
        #sum_p += sum(senti_words[date]["p"].values())
        rf.write(str(date)+"\n")
        #rf.write(str(noun[date])+"\n")
        #rf.write(str(noun_h[date])+"\n")
        #rf.write(str(verb[date])+"\n")
        rf.write(str(senti_words[date]["n"].items())+"\n")
        rf.write(str(senti_words[date]["p"].items())+"\n")
        
sum_n = 0
sum_p = 0
with open("sentir.txt", "w", encoding="utf_8") as rf:
    for date in peak_time_r:
        #sum_n += sum(senti_words[date]["n"].values())
        #sum_p += sum(senti_words[date]["p"].values())
        rf.write(str(date)+"\n")
        #rf.write(str(noun[date])+"\n")
        #rf.write(str(noun_h[date])+"\n")
        #rf.write(str(verb[date])+"\n")
        rf.write(str(senti_words[date]["n"].items())+"\n")
        rf.write(str(senti_words[date]["p"].items())+"\n")
        
#print("ネガティブ："+str(sum_n))
#print("ポジティブ："+str(sum_p))

template = """この話題は {} 頃からtwitter上で話題になり、当初は{}な意見が多く見られました。
その後、{}がきっかけで{}頃から急激に投稿が増え、{}にはピークを迎えます。
この時点では{}な投稿が多く見られます。"""
#result     = template.format()「日付、ポジネガ、原因、日付、ポジネガ」



