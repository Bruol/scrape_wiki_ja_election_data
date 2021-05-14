import requests
from bs4 import BeautifulSoup as bs


file = open('test.txt', 'a')

url = "https://ja.wikipedia.org/wiki/%E7%AC%AC42%E5%9B%9E%E8%A1%86%E8%AD%B0%E9%99%A2%E8%AD%B0%E5%93%A1%E7%B7%8F%E9%81%B8%E6%8C%99#%E5%B0%8F%E9%81%B8%E6%8C%99%E5%8C%BA%E5%BD%93%E9%81%B8%E8%80%85"

page = requests.get(url)

soup = bs(page.content, 'html.parser')

all_links = soup.select('a')

for link in all_links:
    if len(link.contents) == 0:
        link.decompose()
    elif link.contents[0] == "1区":
        link = "https://ja.wikipedia.org" + link['href'] + "\n"
        file.write(link)

file.close