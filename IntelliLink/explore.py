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

def explore_links(root, company, board_keyword):
    req = requests.get(root)
    root_soup = BeautifulSoup(req.text, 'html.parser')
    links = []
    relevance = []

    for anchor in root_soup.find_all('a', href=True):
        url = anchor['href']
        if len(url) < 1:
            continue
        if url[0] == '/':
            url = root + url
        if url[0:4] != "http":
            continue
        if '#' in url:
            continue
        if "javascript:void(0)" in url:
            continue
        if "mailto" in url:
            continue
        if "pdf" in url:
            continue
        print(url)
        if url not in links:
            html = requests.get(url)
            text = text_from_html(html)
            text = text.split()
            length = len(text)
            if length == 0:
                continue
            for kword in board_keyword:
                board_keyword[kword] = text.count(kword.lower())
            links.append(url)
            relevance.append(sum(board_keyword.values()) / length)

    df = pd.DataFrame(data={"Link": links, "Relevance": relevance})
    df = df.sort_values(by='Relevance', ascending=False)
    df.to_csv(company + "_links.csv", index=False)


board_keyword = {"title": 0, "director": 0, "board": 0, "executive": 0, "business": 0,
                 "chief": 0, "group": 0, "global" :0, "officer": 0, "commmittee": 0, "member": 0,
                 "governance": 0, "experience": 0}

explore_links("https://www.reckitt.com/", "Reckitt", board_keyword)
explore_links("https://www.compass-group.com/", "Compass Group", board_keyword)
explore_links("https://www.lseg.com/", "London Stock Exchange Group", board_keyword)
explore_links("https://www.hsbc.com/", "HSBC", board_keyword)
explore_links("https://www.astrazeneca.com/", "Astrazenaca", board_keyword)