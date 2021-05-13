import time
import requests
from bs4 import BeautifulSoup as bs
import json


def extract_line_data(line):
    cols = line.select('td')
    #get party
    party = cols[3].contents[0]
    #clean up party data
    try:
        if party.select('a') != None:
            party = party.contents[0]
    except:
        pass
    # get percentage
    percentage = cols[6].contents[0].contents[1].contents[0]
    return party,percentage

def find_correct_tables(tables,prefecture):
    # needed later
    i = 0
    # iterate over tables
    for table in tables:
        # iterate over lines intable
        lines = table.select('tr')
        #search firs line, first col for 当落
        cols = lines[0].select('th')
        # all the tables we are interested in have 10 collumns
        if len(cols) == 10:
            for col in cols:
                if len(col) == 0:
                    table.decompose()
                elif col.contents[0] == "当落":
                    ldp_percentage = 0
                    temp = ''
                    # get values for first line
                    party,percentage = extract_line_data(lines[1])
                    # if first party is LDP
                    if party == "自由民主党":
                        ldp_percentage = percentage
                        party, percentage = extract_line_data(lines[2])
                    else:
                        # if ldp is not first party, find ldp
                        for j in range(2,len(lines)):
                            temp, ldp_percentage = extract_line_data(lines[j])
                            if(temp == "自由民主党"):
                                break
                    # format data into dictionary
                    prefecture = format_data(years[i],party,percentage,ldp_percentage,prefecture)
                    #needed for year index
                    i += 1
                    if i >= 8:
                        # return dictionary with data
                        return prefecture
    # return dictionary with data
    return prefecture
                
def format_data(year,party,percentage,ldp_percentage,prefecture):
    prefecture[prefecture_num][district_num][year] = {
        'second-party' : {
            'party' : party,
            'percentage' : percentage
            },
        'LDP' : ldp_percentage
        }
    return prefecture
                
years = ["2017","2014","2012","2009","2005","2003","2000","1996"]

prefecture_num = 1

# initialize dictionary
prefecture = {
    prefecture_num :{
    }
}


for district_num in range(1,13):
    prefecture[prefecture_num][district_num] = {}
    
    url = "https://ja.wikipedia.org/wiki/%E5%8C%97%E6%B5%B7%E9%81%93%E7%AC%AC{}%E5%8C%BA".format(district_num)

    page = requests.get(url)

    soup = bs(page.content, 'html.parser')


    #select all tables on page
    tables = soup.select('table')

    prefecture = find_correct_tables(tables,prefecture)


print(json.dumps(prefecture, sort_keys=False, indent=4))
