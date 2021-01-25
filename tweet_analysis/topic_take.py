import urllib.request
from bs4 import BeautifulSoup
import pandas as pd, math
from pathlib import Path
from http.client import RemoteDisconnected

"""
p = Path("/RYO/research/twitter/sakura_url/")

url_dict = {}

for i in p.glob("*"):
    date   = i.name.split("_",2)[2].split(".")[0]
    url_dict[date] = {}
    df     = pd.read_csv(i, encoding="utf_8")
    df2    = df.dropna(how="any")
    
    df_url = df.article
    for u in df_url:
        if isinstance(u, float):
            continue
        else:
            if u in url_dict[date].keys():
                url_dict[date][u] += 1
            else:
                url_dict[date][u]  = 1

        

with open("url_dict.txt", "w", encoding="utf_8") as wf:
    for i in url_dict.keys():
        wf.write(i+"\n")
        for n, url in enumerate(sorted(url_dict[i].items(), key = lambda x: x[1], reverse=True)[:3]):
            print(url)
            try:
                f = urllib.request.urlopen(url[0])
            except urllib.error.HTTPError as e:
                print(e.code)
                continue
            html = f.read().decode('utf-8')

            soup = BeautifulSoup(html, "html.parser")
            wf.write(soup.title.string)
            wf.write("\n")
        wf.write("\n")
        print("hello")
    
#この場合だとurlに日本語が含まれている場合に対応していないので注意
#日本語をasciiに変換する"""

def midashi(url):
    try:
        f = urllib.request.urlopen(url)
        try:
            html = f.read().decode('utf-8')
        except:
            html = f.read().decode('shift-jis')
            
        soup = BeautifulSoup(html, "html.parser")
        try:
            return str(soup.title.string)
        except:
            return "削除済み"
    except (urllib.error.HTTPError,RemoteDisconnected) as e:
        return "削除済み"
