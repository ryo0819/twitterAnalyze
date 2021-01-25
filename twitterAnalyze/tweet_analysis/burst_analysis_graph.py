"""
burst_analysisで得た情報を視覚化
"""


import matplotlib.pyplot as plt, matplotlib as mpl
import numpy as np, pandas as pd

#ewmを計算
def outlier(ts, alpha, threshold=2.0):
    assert type(ts) == pd.Series
    ewm_mean = ts.ewm(alpha=alpha).mean()
    ewm_std  = ts.ewm(alpha=alpha).std()
    outer = ts[(ts - ewm_mean) > ewm_std*threshold]
    return outer
                
#グラフ化
def plot_outlier(ts, out_url, out_index, out_values, alpha):
    assert type(ts) == pd.Series
    fig, ax  = plt.subplots()
    annot = ax.annotate("", xy=(0,0), xytext=(10,10),textcoords="offset points", arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    ewm_mean = ts.ewm(alpha).mean()
    ewm_std  = ts.ewm(alpha).std()
    
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


