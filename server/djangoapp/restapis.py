import requests
import json
from .models import *
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, headers={'Content-Type': 'application/json'}):
    
    # try:
        # Call get method of requests library with URL and parameters
    # return json_payload
    response = requests.post(url, json=json_payload, auth=HTTPBasicAuth('apikey', 'uxIts40B9NC9zz_J10ZOTtOpUJOcCXoCr1Rxk5apWqT0'))
    # except:
    #     # If any error occurs
    #     print("Network exception occurred")
    status_code = response.status_code
    print(f"With status {status_code}")
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(param=""):
    results = []
    url = "https://olivernadela-3000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai"
    url = f"{url}/dealerships/get"
    if param:
        url = f"{url}/{param}"

    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        sorted_dealers = sorted(dealers, key=lambda x : x['id'])
        # For each dealer object
        for dealer in sorted_dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def get_dealer_by_id_from_cf(dealerID):
    # - Call get_request() with specified arguments
    # - Parse JSON results into a DealerView object list
    param = f"?id={dealerID}"
    return get_dealers_from_cf(param)

def get_dealer_by_state_from_cf(state):
    # - Call get_request() with specified arguments
    # - Parse JSON results into a DealerView object list
    param = f"?state={state}"
    return get_dealers_from_cf(param)

def filter_keys(pair):
    return True
    # key,val = pair
    # unwanted_keys = ['_id','_rev','another']
    # return False if key in unwanted_keys else True

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(id):
    results = []
    url = "https://olivernadela-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai"
    json_result = get_request(f"{url}/api/get_reviews?id={id}")
    if json_result:
        # Get the row list in JSON as reviews
        reviews = json_result
        # list the fields for the object
        objflds = ['id', 'name', 'dealership', 'review', 'car_make', 'car_model', 'car_year', 'purchase', 'purchase_date']
        # For each review object
        for review in reviews:
            newflds = filter(lambda key: key in objflds,review.keys())
            newflds = dict((d,review[d]) for d in newflds)
            review_obj = DealerReview(**newflds)
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return (results)

def dealership_add_review(request, dealer_id):
    id = request.user.id
    name = request.user.get_full_name()
    dealership = dealer_id
    review = request.POST['content']
    car = CarModel.objects.get(id=request.POST['car'])
    car_make = car.car_make.name
    car_model = car.name
    car_year = car.year
    purchase = request.POST["purchasecheck"]
    purchase_date = json.dumps(request.POST["purchasedate"])
    dealer_review_obj = {
        'id':id, 
        'name':name, 
        'dealership':dealership, 
        'review':review, 
        'car_make':car_make, 
        'car_model':car_model, 
        'car_year':car_year, 
        'purchase':purchase, 
        'purchase_date': purchase_date}
    json_payload = dealer_review_obj
    url = "https://olivernadela-5000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
           
    response = post_request(url, json_payload)
    return response

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/3680cd63-7db8-4148-9e07-950fea1936be"
    api_key = "uxIts40B9NC9zz_J10ZOTtOpUJOcCXoCr1Rxk5apWqT0"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text+" hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+" hello hello hello"])), language='en').get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']

    return(label)

