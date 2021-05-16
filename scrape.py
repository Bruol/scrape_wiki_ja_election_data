import requests
from bs4 import BeautifulSoup as bs
import json
import progressbar


years = ["2017","2014","2012","2009","2005","2003","2000","1996"]


# PRE: expects a html table line
# Post returns the party name and percentage of that party
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

# PRE: select tables, with certain Pattern from a webpage
# POST: Returns a list of tables
def find_correct_tables(tables):
    tables_list = []
    # needed later
    i = 0
    # iterate over tables
    for table in tables:
        # iterate over lines in table
        lines = table.select('tr')
        #search firs line, first col for 当落
        cols = lines[0].select('th')
        # all the tables we are interested in have 10 collumns
        if len(cols) == 10:
            for col in cols:
                if len(col) == 0:
                    table.decompose()
                elif col.contents[0] == "当落":
                    tables_list.append(table)
                    #needed for year index
                    i += 1
                    if i >= 8:
                        # return array of correct tables
                        return tables_list
    # return array of tables
    return tables_list

#PRE: A string with Party Name
#Post: returns the percentage for searched party
def get_by_name(party,table):
    # extract lines from table
    lines = table.select('tr')

    for j in range(1,len(lines)):
        temp, percentage = extract_line_data(lines[j])
        if temp == party:
            return percentage
        else:
            percentage = "0"
    return percentage

#PRE: a int index and a table
#POST: returns name and percentage of first party in table
def get_by_index(index,table):
    lines = table.select('tr')

    return extract_line_data(lines[index])

#Pre: filename with the links
#POST: returns a list with the urls for the prefects
def get_urls(filename="./res/prefects.txt"):
    link_list = []

    try:
        with open(filename) as file:
            for line in file:
                link_list.append(line.split('\n')[0])
    except:
        print("opening file did not work")


    return link_list

#Pre: expects a url and an index
#POST: returns url with corresponding index
def format_district_url(index,url):
   return url.split('%AC1')[0] + "%AC" + str(index) + url.split('%AC1')[1]

# Pre: expects party name
# Post: returns the percentage of the party and the best party
def find_party_and_best(ldp):
    
    data = {}
    # read prefecture urls from file
    urls = get_urls()
    # start counting prefectures
    prefecture_num = 1
    
    bar = progressbar.ProgressBar(max_value=len(urls))

    # iterate over prefectures
    for prefec in urls:
        
        bar.update(prefecture_num)

        data[str(prefecture_num)] = {}
        # iterate over districts in prefecture
        district_num = 1
        while True:
            # format the url for the correct district
            url = format_district_url(district_num,prefec)
            # download the page
            page = requests.get(url)
            #check if district exists
            if(page.status_code == 404):
                break
            # parse string as html
            soup = bs(page.content , "html.parser")
            
            data[str(prefecture_num)][str(district_num)] = {}

            #select all tables on page
            tables = soup.select('table')

            # find tables wih election data from wikipedia page
            tables = find_correct_tables(tables)

            # go through each table on page            
            for i in range(0,len(tables)):
                # get data from first line of current tables
                party,percentage = get_by_index(1,tables[i])
                # check if first party is ldp
                if party == ldp:
                    ldp_percentage = percentage
                    party, percentage = get_by_index(2,tables[i])
                # search for ldp
                else:
                    ldp_percentage = get_by_name(ldp,tables[i])
                # save results
                data[str(prefecture_num)][str(district_num)][years[i]] = {
                    "second-party" : {
                        'party' : party,
                        'percentage' : percentage
                    },
                    'LDP' : ldp_percentage
                }
            # go to next district
            district_num += 1
        
        # go to next prefecture
        prefecture_num += 1
    # return data
    return data

# Pre: expects data from findparty_and_best and a filename to a file like res/switch.txt
# Post: rearrange prefects
def swap_prefects(data,filename="./res/switch.txt"):
   
    s_file = open(filename, 'r')

    data_dest = data.copy()

    for line in s_file:
        pdf,wiki = line.split('-')
        wiki = wiki.split('\n')[0]
        prefecture_wiki = data[wiki]
        data_dest[pdf] = prefecture_wiki

    s_file.close()

    return data_dest

# Pre: expects data from find_party_and_best
# Post: creates csv file from data
def gen_csv(data,external=False,title=('Prefecture','District','year','LDP_Percentage','Other Party Percentage'),filename="./results/results.csv"):
    import csv

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(title)

        if external:
            for prefec in data:
                for district in data[prefec]:
                    for year in data[prefec][district]:
                        writer.writerow((prefec,district,year,data[prefec][district][year]['percentage']))
        else:     
            for prefec in data:
                for district in data[prefec]:
                    for year in data[prefec][district]:
                        writer.writerow((prefec,district,year,data[prefec][district][year]['LDP'],data[prefec][district][year]['second-party']['percentage']))

def get_party_data(party):
    
    data = {}
    # read prefecture urls from file
    urls = get_urls()
    # start counting prefectures
    prefecture_num = 1
    
    bar = progressbar.ProgressBar(max_value=len(urls))

    # iterate over prefectures
    for prefec in urls:
        
        bar.update(prefecture_num)

        data[str(prefecture_num)] = {}
        # iterate over districts in prefecture
        district_num = 1
        while True:
            # format the url for the correct district
            url = format_district_url(district_num,prefec)
            # download the page
            page = requests.get(url)
            #check if district exists
            if(page.status_code == 404):
                break
            # parse string as html
            soup = bs(page.content , "html.parser")
            
            data[str(prefecture_num)][str(district_num)] = {}

            #select all tables on page
            tables = soup.select('table')

            # find tables wih election data from wikipedia page
            tables = find_correct_tables(tables)

            # go through each table on page            
            for i in range(0,len(tables)):
                percentage = get_by_name(party,tables[i])
                # save results
                data[str(prefecture_num)][str(district_num)][years[i]] = {
                    'percentage' : percentage
                }
            # go to next district
            district_num += 1
        
        # go to next prefecture
        prefecture_num += 1
    # return data

    data_swapped = swap_prefects(data)

    # file = open('./results/'+party+'.json', 'w')
    # file.write(json.dumps(data_swapped, sort_keys=False, indent=4))
    # file.close

    gen_csv(data_swapped,external=True,title=('Prefecture','District','year',party),filename='./results/'+party+'.csv')

    return data



if __name__ == "__main__":
    # party searched for
    ldp = "自由民主党"

    data = find_party_and_best(ldp)

    print("\n swapping prefecture numbers\n")

    data_swapped = swap_prefects(data)

    print("save results to ./results/results.json\n\n")

    file = open('./results/results.json', 'w')
    file.write(json.dumps(data_swapped, sort_keys=False, indent=4))
    file.close

    print("generating csv from data")

    gen_csv(data_swapped)

    print("\n\n\n successfully written fata to results.json \n\n Hoorayyy!!!")


