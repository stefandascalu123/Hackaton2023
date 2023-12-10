# Description: This is the main file for the project.

# import files
import api_calls
import os
import math

#import modules
import json
import data_analysis

def get_best_matches(company):
    # main function
    #payload = api_calls.create_payload_match(commercial_names = ["Google"], website= "google.com")
    response = api_calls.api_match_request(company)
    # response_pretty = json.dumps(response, indent=4, sort_keys=True)
    # print(response_pretty)
    locations = data_analysis.get_locations(response)
    business_tags = data_analysis.get_category(response)

    #print(locations[len(locations)-1])
    competitors = api_calls.search_competitors(locations[0], business_tags)
    #print(competitors["count"])
    #print(locations[2]["city"])
    #rows = data_analysis.get_population(locations[0]["city"])
    #comp_coef = (competitors["count"]/rows[0][0]) * 1000
    #print(comp_coef)
    lat_med, lng_med = data_analysis.compute_median(locations)
    print(data_analysis.get_max_distance(locations))
    if lat_med == 200 and lng_med == 200:
        with open('err', 'w') as file:
            json.dump("No locations found", file)
        return
    #print(data_analysis.compute_median(locations))
    #print(locations)
    jason = data_analysis.get_possible_locations(lat_med, lng_med, 3)

    scores = []
    locs = []
    max_comp = 0
    max_population = 0
    comps = []
    succs = []

    for loc in jason:
        locs.append(loc)
        scores.append(0)
        succs.append(0)
        dicts = json.loads(loc)
        comp = api_calls.search_competitors(dicts, business_tags)
        comps.append(comp["count"])
        if comp["count"] > max_comp:
            max_comp = comp["count"]
        if dicts["population"] > max_population:
            max_population = dicts["population"]

    for i in range (len(comps)):
        comp_coef = (max_comp - comps[i])/max_comp
        pop_coef = json.loads(locs[i])["population"]/max_population
        for loc in locations:
            if loc["city"] == json.loads(locs[i])["city"]:
                succs[i] += 1
        succ_coef = (len(locations) - succs[i])/len(locations)
        scores[i] = succ_coef
        scores[i] = comp_coef * 0.4 + pop_coef * 0.4 + succ_coef * 0.2
    
    for i in range(len(scores)):
        for j in range(i+1, len(scores)):
            if scores[i] < scores[j]:
                aux = scores[i]
                scores[i] = scores[j]
                scores[j] = aux
                aux = locs[i]
                locs[i] = locs[j]
                locs[j] = aux
    output = []
    for i in range(len(scores)):
        if i > 4:
            break
        #print(scores[i], locs[i])
        output.append({
            "score": scores[i],
            "city": json.loads(locs[i])["city"],
            "country": json.loads(locs[i])["country"],
        })

    print(output)
    with open('output.json', 'w') as file:
        json.dump(output, file)


def main():
    
    while (True):
        if (os.stat("data.json").st_size == 0):
            continue
        with open('data.json') as json_file:
            open('output.json', 'w').close()
            open('err', 'w').close()
            print("nu mai intind mana")
            data = json.load(json_file)
            get_best_matches(data)
        open('data.json', 'w').close()
        print("am intins mana")
 
    

if __name__ == '__main__':
    main()