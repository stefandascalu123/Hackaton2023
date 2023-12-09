# Description: This is the main file for the project.

# import files
import api_calls

#import modules
import json

match_payload_empty = {
                        "legal_names": [],
                        "commercial_names": [
                            "Factset"
                        ],
                        "address_txt": "Connecticut, United States",
                        "phone_number": "",
                        "website": "factset.com"
                    }

search_payload_empty = {
                            "filters": {
                                "and": [
                                    {
                                        "attribute": "company_website",
                                        "relation": "in",
                                        "value": ["bcg.com", "accenture.com"]
                                    }
                                ]
                            }
                        }

def main():
    #main function
    payload = api_calls.create_payload_match(commercial_names = ["Factset"], address_txt = "Connecticut, United States", website= "factset.com")
    response = api_calls.api_match_request(payload)
    print(json.dumps(response, indent=4, sort_keys=True))


if __name__ == '__main__':
    main()