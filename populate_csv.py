import json
import csv

data_f = open('results_swapped.json')
data = json.load(data_f)
data_f.close()

with open('results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(('Prefecture','District','year','LDP_Percentage','Other Party Percentage'))
    
    for prefec in data:
        for district in data[prefec]:
            for year in data[prefec][district]:
                writer.writerow((prefec,district,year,data[prefec][district][year]['LDP'],data[prefec][district][year]['second-party']['percentage']))
