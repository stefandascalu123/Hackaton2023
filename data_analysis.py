import json

def get_locations(json):
    # code to get locations from json
    locations = json["locations"]
    return locations

def get_category(json):
    # code to get business tags from json
    business_tags = json["main_business_category"]
    return business_tags

def get_num_of_competitors(competitors):
    # code to get number of competitors from json
    num_of_competitors = competitors["count"]
    return num_of_competitors