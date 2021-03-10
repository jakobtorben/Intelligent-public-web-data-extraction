import requests
from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas as pd

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(html):
    soup = BeautifulSoup(html.text, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts).lower()

root = "https://www.astrazeneca.com/"
req = requests.get("https://www.astrazeneca.com/")
root_soup = BeautifulSoup(req.text, 'html.parser')
board_keyword = {"committee": 0, "board": 0, "officer": 0, "executive": 0, "leadership": 0,
                 "non-executive": 0, "CEO": 0, "CFO" :0, "chief": 0, "director": 0, "directors": 0, "governace": 0}
links = []
relevance = []

for anchor in root_soup.find_all('a', href=True):
    url = anchor['href']
    if url[0] == '/':
        url = root + url
    if url[0:4] != "http":
        continue
    print(url)
    if url not in links:
        html = requests.get(url)
        text = text_from_html(html)
        text = text.split()
        for kword in board_keyword:
            board_keyword[kword] = text.count(kword.lower())
        links.append(url)
        relevance.append(sum(board_keyword.values()))


df = pd.DataFrame(data={"Link": links, "Relevance": relevance})
df = df.sort_values(by='Relevance', ascending=False)
df.to_csv("./Astrazenaca_links.csv", index=False)
