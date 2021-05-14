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
                    ldp_percentage = "0"
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
                            else:
                                ldp_percentage = "0"
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

link_list = []

try:
    with open('test.txt') as file:
        for line in file:
            link_list.append(line.split('\n')[0])
except:
    print("opening file did not work")

prefecture_num = 1

# initialize dictionary
prefecture = {}

for prefec in link_list:
    prefecture[prefecture_num] = {}
    print("\n\n\ngetting data from prefecture no. " + str(prefecture_num) + "\n")
    district_num = 1
    while True:
        
        print("         getting data from pref. no. {} district no. {}".format(prefecture_num,district_num) )

        url = prefec.split('%AC1')[0] + "%AC" + str(district_num) + prefec.split('%AC1')[1]

        page = requests.get(url)

        if(page.status_code == 404):
            break

        soup = bs(page.content, 'html.parser')
        
        prefecture[prefecture_num][district_num] = {}

        #select all tables on page
        tables = soup.select('table')

        prefecture = find_correct_tables(tables,prefecture)

        district_num += 1

    prefecture_num += 1

file = open('results.json', 'w')
file.write(json.dumps(prefecture, sort_keys=False, indent=4))
file.close

print("\n\n\n successfully written fata to results.json \n\n Hoorayyy!!!")

quit()