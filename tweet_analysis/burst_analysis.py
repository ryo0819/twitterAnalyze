import MeCab, matplotlib.pyplot as plt, matplotlib as mpl
import numpy as np, pandas as pd
from gensim.models import word2vec
import nakamura, re, math
sentiments = nakamura.sentiments
from convinience_method import my_print, sub_text
from topic_take import midashi

import burst_analysis_graph
#import statsmodels.api as sm
#pd.options.display.max_columns = None#ここを追加するとdataframeが省略されない

model = word2vec.Word2Vec.load("wiki.model")

#MeCab宣言
mt    = MeCab.Tagger(r"C:\progra~1\MeCab\etc\mecabrc")
mt.parse("")

"""#月ごとに見たとき（実験用）
file_name = "桜を見る会_2019-10-01to2019-10-31"
df1       = pd.read_csv(file_name+".csv", encoding="utf_8")
file_name = "桜を見る会_2019-11-01to2019-11-30"
df2     = pd.read_csv(file_name+".csv", encoding="utf_8")
file_name = "桜を見る会_2019-12-01to2019-12-31"
df3       = pd.read_csv(file_name+".csv", encoding="utf_8")
df = pd.concat([df1,df2, df3], axis=0)"""

#分析ファイル指定
file_name    = "渡部健_2020-06-08to2020-06-10"
df           = pd.read_csv(file_name+".csv", encoding="utf_8")

#ファイル名の検索ワードを取得&ノード数を取得
#のちにノード数を使って文章を分割
try:
    keyword = file_name.split("_")[0]
except:
    try:
        keyword = file_name.split("_")[6]
    except:
        print("ファイル名の形式が当てはまりません")
        exit()

node       = mt.parseToNode(keyword)
node_count = 0
while node:
    if node.feature.startswith("BOS/EOS"):
        node = node.next
        continue
    node_count += 1
    node = node.next
print(keyword+"："+str(node_count))

#「年,月,日_時間」をキーとしてアクセスするための処理
date_time_list = []#日付_時間
date_list        = []#日付
list_frames     = {}

for n, row in enumerate(df.itertuples()):
    try:
        i = row.created.split(" ")[0] +"_" + row.created.split(" ")[1].split(":")[0]
    except:
        continue
    if i in date_time_list:
        continue
    else:
        if not date_time_list:
            change = n
            if re.match(r"^\d{4}\/\d{2}\/\d{2}", i):
                cdate = i
                date_time_list.append(i)
            elif re.match(r"^\d{4}-\d{2}-\d{2}", i):
                cdate = i
                date_time_list.append(i)
        else:
            """print(cdate)
            print(n-1)
            input()"""
            list_frames[cdate] = df[change:n]
            change = n
            if re.match(r"^\d{4}\/\d{2}\/\d{2}", i):
                cdate = i
                date_time_list.append(i)
            elif re.match(r"^\d{4}-\d{2}-\d{2}", i):
                cdate = i
                date_time_list.append(i)
                
#データフレームを辞書に格納
list_frames[i] = df[change:n+1]
alpha          = 2 / (len(list_frames)+1)

#日ごとのツイート数
"""tweet_sum = {}
for date in date_list:
    sum_t = 0
    for time in date_time_list:
        if re.match(date, time):
            sum_t += tweet_time_count[time]
    tweet_sum[date] = sum_t"""

"""
#ewmを計算
def outlier(ts, alpha=alpha, threshold=2.0):
    assert type(ts) == pd.Series
    ewm_mean = ts.ewm(alpha=alpha).mean()
    ewm_std  = ts.ewm(alpha=alpha).std()
    outer = data[(data - ewm_mean) > ewm_std*threshold]
    return outer
                
#グラフ化
def plot_outlier(ts, out_url, out_index, out_values, alpha=alpha):
    assert type(ts) == pd.Series
    fig, ax  = plt.subplots()
    annot = ax.annotate("", xy=(0,0), xytext=(10,10),textcoords="offset points", arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    ewm_mean = ts.ewm(alpha=alpha).mean()
    ewm_std  = ts.ewm(alpha=alpha).std()
    
    ax.plot(ts, label="ツイート数")
    ax.plot(ewm_mean, label="指数加重移動平均", linewidth=3)
    sc=ax.scatter(out_index, out_values, label="盛り上がり", color="red", linewidths=5)
    
    plt.xticks(out_index, [re.split("-|_",t)[2] +"\n日\n" + re.split("-|_",t)[3] +"\n時" for t in out_index], fontsize=10)
    #plt.xticks(x[:500:30], [re.split("-|_",t)[2] +"\n日\n" + re.split("-|_",t)[3] +"\n時" for t in x[::30]], fontsize=1)
    plt.yticks(fontsize=15)

    plt.legend(fontsize=20)

    # アノテーション表示更新
    def update_annot(ind):
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = "\n".join(map(str, out_url[ind["ind"][0]]))#この部分に記事の見出しと感情を入れたい
        annot.set_text(text)

    # hoverイベント
    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax: # 上下移動や虫眼鏡のドラッグ中は探さない
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()
    fig.canvas.mpl_connect("motion_notify_event", hover)
    plt.show()
"""
    
#日ごとに見るとき
#x = list(tweet_sum.keys())
#y = list(tweet_sum.values())

#時間ごとに見て外れ値を持つ日時を出す
x = list(list_frames.keys())
y = [len(list_frames[count]) for count in list_frames.keys()]
data = pd.Series(y,x)#日付が降順のデータ
out  = burst_analysis_graph.outlier(data, alpha)

out_index = list(out.index)#最終的に外れ値にの日時になる
out_values = list(out.values)
out_sorted = sorted(out_index)
out_list = []

"""for o in out_sorted:
    t_list = o.split("_")
    if not t_list[0] in out_list:
        out_list.append(t_list[0])
    else:
        out_values.pop(out_index.index(o))
        out_index.remove(o)
#ここまでで外れ値を持つ日時を検出
#外れ値の日付を可視化"""
list_frames = dict(sorted(list_frames.items(), key=lambda x:x[0],reverse=False))
x = list(list_frames.keys())
y = [len(list_frames[count]) for count in list_frames.keys()]
data1 = pd.Series(y,x)#日付が昇順のデータ


#該当する日時の見出し＆感情分析
out_url   = {}
out_senti = {}
na_phrase = {}
top_three_u = {}
top_three_s = {}
exclude     = {}
remain      = {}
nakamura_sentiments = {0:"哀",1:"恥",2:"怒",3:"嫌",4:"怖",5:"驚",6:"昂",7:"好",8:"安",9:"喜"}


for date in out_index:
    out_url[date]   = {}
    out_senti[date] = {}
    remain[date]    = []
    exclude[date]   = []
    na_phrase[date] = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
    #外れ値の日付のurlを取得
    for url in list_frames[date].quote_url:
        try:
            if math.isnan(url):
                continue
            else:
                if url in out_url[date].keys():
                    out_url[date][url] += 1
                else:
                    out_url[date][url]  = 1
        except:
            if url in out_url[date].keys():
                out_url[date][url] += 1
            else:
                out_url[date][url]  = 1
    out_url[date] = dict(sorted(out_url[date].items(), key=lambda x:x[1], reverse=True))
    top_three_u[date] = [sw[0] for n, sw in enumerate(out_url[date].items()) if n < 3]
    print(date)
    print(top_three_u[date])

    #外れ値の日付の感情語を取得
    for text in list_frames[date].text:
        if re.search(keyword, str(text)):
            text_splited = text.split(keyword)
            for l in text_splited:
                node = mt.parseToNode(l)
                while node:
                    fields = node.feature.split(",")#品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
                    node = node.next
                    if  fields[0] == "形容詞" or "形容詞" in fields[1] or fields[0] == '動詞' or fields[0] == '名詞':
                        for n, sentiment in enumerate(sentiments):
                            if fields[6] in sentiment:
                                if not fields[6] in out_senti[date].keys():
                                    na_phrase[date][n]         += 1
                                    out_senti[date][fields[6]]  = 1
                                else:
                                    na_phrase[date][n]         += 1
                                    out_senti[date][fields[6]] += 1

    #感情語の日別の違いをリストに→excludeを日別にすることで前日との差を見ることができる
    for p in list(out_senti[date].keys()):
        if p in exclude[date]:
            continue
        else:
            remain[date].append(p)
            exclude[date].append(p)

    out_senti[date] = dict(sorted(out_senti[date].items(), key=lambda x:x[1], reverse=True))
    top_three_s[date] = [sw for n, sw in enumerate(out_senti[date].items()) if n < 3]

    #print(date)
    #print(top_three_s[date])
    #print(remain[date])
    print(na_phrase[date])

burst_analysis_graph.plot_outlier(data1, list(top_three_u.values()), out_index, out_values, alpha)#グラフ出現








