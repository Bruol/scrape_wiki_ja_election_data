from scrape import get_party_data


party = input("Which Party do you want to search for? : ")


print("getting data for "+party)

get_party_data(party)

print("\n saved results into ./results/"+ party + ".csv" )