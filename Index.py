#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def get_api_key(username, password):
    """API call to get an API key to use in future requests."""
    method = "POST"
    url = BASE_URL + "v4/account/authenticate/"
    parameters = {"apikey": "androidble"}
    body = {
     "username": username,
     "password": password
    }
    response_json = call_api(method, url, parameters, body)
    return response_json["Token"]


# In[ ]:


def get_products(username, api_key):
    """API call to get a list of products registered with the account."""
    method = "GET"
    url = BASE_URL + "v4/product?complex=true"
    parameters = {
        "username": username,
        "apikey": api_key
    }
    response_json = call_api(method, url, parameters)

    products = []
    for product in response_json:
        products.append({
            "name": product["Name"],
            "product_id": product["Id"],
            "device_id": product["KMSDevice"]["DeviceId"],
            "KMS_id": product["KMSDevice"]["Id"],
            "latitude": product["KMSDevice"]["Location"]["Latitude"],
            "longitude": product["KMSDevice"]["Location"]["Longitude"],
            "primary_code": product["KMSDevice"]["PrimaryCode"],
            "model_id": product["Model"]["Id"],
            "model_name": product["Model"]["Name"],
            "model_number": product["Model"]["ModelNumber"],
            "model_SKU": product["Model"]["SKU"]
        })
    return products


# In[ ]:


def generate_temporary_code(username, api_key, kms_id, access_time=None):
    """API call to generate a temporary code. If access_time is None, gets a currently active code."""
    method = "GET"
    url = BASE_URL + "v4/kmsdevice/" + kms_id + "/servicecode/"
    parameters = {
        "username": username,
        "apikey": api_key
    }
    if access_time is not None:
        parameters["accessTime"] = access_time
    response_json = call_api(method, url, parameters)
    return response_json["ServiceCode"]


# In[ ]:


BASE_URL = "https://api.masterlockvault.com"
USER = ""
PASS = ""
API_KEY = get_api_key(USER, PASS)
products = get_products(USER, API_KEY)
codes = []
for product in products:
    codes.append(generate_temporary_code(USER, API_KEY, product["KMS_id"]))
print(codes)

