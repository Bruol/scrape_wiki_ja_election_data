import json

s_file = open('notes.md', 'r')

f_data = open('results.json')
data = json.load(f_data)
f_data.close()

data_dest = data.copy()


for line in s_file:
    pdf,wiki = line.split('-')
    wiki = wiki.split('\n')[0]
    prefecture_wiki = data[wiki]
    data_dest[pdf] = prefecture_wiki


s_file.close()

results = open('results_swapped.json', "w")

results.write(json.dumps(data_dest, sort_keys=False, indent=4))

results.close()