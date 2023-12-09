# Description: This is the main file for the project.

# import files
import api_calls

#import modules
import json
import data_analysis

def main():
    # main function
    payload = api_calls.create_payload_match(commercial_names = ["Factset"], address_txt = "Connecticut, United States", website= "factset.com")
    response = api_calls.api_match_request(payload)
    # response_pretty = json.dumps(response, indent=4, sort_keys=True)
    # print(response_pretty)
    locations = data_analysis.get_locations(response)
    business_tags = data_analysis.get_category(response)

    print(locations[len(locations)-1])
    competitors = api_calls.search_competitors(locations[2], business_tags)
    print(competitors["count"])
    

if __name__ == '__main__':
    main()