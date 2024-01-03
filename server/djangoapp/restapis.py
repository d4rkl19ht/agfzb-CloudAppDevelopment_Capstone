import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(param):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
    response = requests.get(f"https://olivernadela-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get?{param}")
    return response.json



# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(dealerId):# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
    response = requests.get(f"https://olivernadela-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews?id={dealerId}")
    return response.json

def dealership_add_review(request,review):
    context = {}
    # review = {
    #     "id": 1114,
    #     "name": "Upkar Lidder",
    #     "dealership": 15,
    #     "review": "Great service!",
    #     "purchase": False,
    #     "purchase_date": "02/16/2021",
    #     "car_make": "Audi",
    #     "car_model": "Car",
    #     "car_year": 2021
    # }
    url = "https://olivernadela-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
    response = requests.post(url, json=review)
    return response

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



