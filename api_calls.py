# Description: This file contains the code to make API calls to Veridion API
import requests
import json

# API key for Veridion API
match_key = "Lk34BnMBMFDj07xGbkQ_aNikeD4_NSKq643WxEEuQUAcjtbrVJStX9FpASw7"
search_key = "pXStedvXkA9pMcNK1tWvx_4DesmTsIZ47qfTa6WkqFxgrCvCqJA0mpALQ53J"

# API URL for Veridion API
match_url = "https://data.veridion.com/match/v4/companies"
search_url = "https://data.veridion.com/search/v2/companies"


# API Headers for Veridion API
header_match= {
    "x-api-key": match_key,
    "accept": "application/json",
    "content-type": "application/json"
}

header_search= {
    "x-api-key": search_key,
    "accept": "application/json",
    "content-type": "application/json"
}

def create_payload_match(legal_names = [], commercial_names = [], address_txt = "", phone_number = "", website= ""):
    # code to create payload for match API call
    payload = {
                "legal_names": legal_names,
                "commercial_names": commercial_names,
                "address_txt": address_txt,
                "phone_number": phone_number,
                "website": website
            }
    return payload


def search_competitors(location, category):
    # operand1 = "{\"attribute\": \"company_category\",\"relation\": \"in\", \"value\": {\"operator\": \"or\",\"operands\": [\"" + '\", \"'.join(str(e) for e in business_tags) + "\"]}}"
    # operand2 = "{\"attribute\": \"company_location\",\"relation\": \"in\", \"value\": {\"country\": " + json.dumps(location["country"]) + ",\"region\": " + json.dumps(location["region"]) + ",\"city\": " + json.dumps(location["city"]) + "}}"
    # #payload = "{\"filters\":{\"and\": [" + operand1 + ", " + operand2 + "]}}"

    joan = {
        "filters": {
            "and": [
                {
                    "attribute": "company_category",
                    "relation": "equals",
                    "value": category
                }
                ,
                {
                    "attribute": "company_location",
                    "relation": "equals",
                    "value": {
                        "country": location["country"],
                        "region": location["region"],
                        "city": location["city"]
                }
            }
        ]
    }
}
    response = api_search_request(joan, 10)
    print(response)
    return response

def api_match_request(payload):
    # code to make API call to Veridion API
    response = requests.post(match_url, json=payload, headers=header_match)
    ret = json.loads(response.text)
    return ret

def api_search_request(payload, page_size):
    # code to make API call to Veridion API
    if page_size == 0:
        url = search_url
    else:
        url = search_url + "?page_size=" + str(page_size)
    response = requests.post(url, json=payload, headers=header_search)
    ret = json.loads(response.text)
    return ret