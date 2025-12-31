import json
import requests
import os
url = os.enviorn.get('REQUEST_URL')
endpoint = os.environ.get('REQUEST_ENDPOINT')

def get_data(url,endpoint):
    try:
        response = requests.get(url + endpoint)
        response.raise_for_status()
        data = response.json()
        return data
        print(f"Successfully fetched data from {url}{endpoint}.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON from the response.")

def transform_dogs():
    try:
        data = get_data(url,endpoint)
        try:
            dog_breeds = []
            for breed_name in data['message'].keys():
                dog_breeds.append(breed_name)
        except:
            print("Error determining dog breeds.")
        try:
            output = []
            for index,breed_name in enumerate(dog_breeds):
                output.append({'breed':breed_name,'sub_breeds':data['message'][dog_breeds[index]]})
            return output
        except:
            print("Error creating output.")
    except:
        print("Error")
        raise

