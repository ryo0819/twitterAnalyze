from pathlib import Path

p = Path("C:/research/ishikawa/akira_nakamura_sentiments")
sentiments = []

for i in p.glob("*"):
    temp_list = []
    with open(i, "r", encoding="utf_8") as rf:
        for line in rf:
            line = line.strip()
            temp_list.append(line)
        sentiments.append(temp_list)
