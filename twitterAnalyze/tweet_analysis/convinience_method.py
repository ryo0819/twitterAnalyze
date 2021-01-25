import re, sys

def my_print(text):
    try:
        print(text)
    except UnicodeEncodeError as e:
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)  #「https://teratail.com/questions/90318」を参考に。
        trans_text = str(text).translate(non_bmp_map)
        trans_text = re.sub("�", "", trans_text)
        print(trans_text)

#テキストを校正
def sub_text(text):
    re_text = re.sub("�", "", text)
    re_text = re.sub(r"\n", "", re_text)
    re_text = re.sub(r"@\w+", "", re_text)
    re_text = re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+\$,%#]+)", "", re_text)
    re_text = re_text.strip()
    return re_text


