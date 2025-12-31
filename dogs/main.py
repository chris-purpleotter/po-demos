import json
import requests
import os
import random
from google.cloud import storage
url = os.environ.get('REQUEST_URL')
endpoint = os.environ.get('REQUEST_ENDPOINT')
storage_client = os.environ.get('STORAGE_CLIENT')
storage_bucket = os.environ.get('STORAGE_BUCKET')

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
            output.append({'breed':'UNKNOWN','sub_breeds':[str(random.randint(1, 10000)),str(random.randint(1, 10000))]})
            with open('transactions.json','w',encoding='utf-8') as f:
                for i in output:
                    json.dump(i,f)
                    f.write('\n')
                f.close()
                file_path = 'automated_load'
                file_name = 'dogs.json'
                gcp_storage_client = storage.Client(storage_client)
                gcp_storage_bucket = gcp_storage_client.bucket(storage_bucket)
                file_upload = gcp_storage_bucket.blob(file_path + '/' + file_name)
                file_upload.upload_from_filename(file_name)    
            print(output)
        except:
            print("Error creating output.")
    except:
        print("Error")
        raise
