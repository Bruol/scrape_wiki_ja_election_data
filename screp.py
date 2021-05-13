import time
import requests
from bs4 import BeautifulSoup as bs

years = ["2017","2014","2012","2009","2005","2003","2000","1996"]

district_num = 1

url = "https://ja.wikipedia.org/wiki/%E5%8C%97%E6%B5%B7%E9%81%93%E7%AC%AC{}%E5%8C%BA".format(district_num)

page = requests.get(url)

soup = bs(page.content, 'html.parser')

def extract_first_line_data(line):
    cols = line.select('td')
    party = cols[3].contents[0]
    percentage = cols[6].contents[0]


def find_correct_table(tables):
    # iterate over tables
    for table in tables:
        # iterate over lines intable
        lines = table.select('tr')
        #search firs line, first col for 当落
        cols = lines[0].select('th')
        for col in cols:
            if len(col) == 0:
                table.decompose()
            elif col.contents[0] == "当落":
                print('found table')
                extract_first_line_data(lines[1])




#select all tables on page
tables = soup.select('table')

find_correct_table(tables)