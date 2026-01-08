import json
import requests
import os
from google.cloud import storage
url = os.environ.get('REQUEST_URL')
endpoint = os.environ.get('REQUEST_ENDPOINT')
storage_client = os.environ.get('STORAGE_CLIENT')
storage_bucket = os.environ.get('STORAGE_BUCKET')

def get_data(url,endpoint):
    try:
        response = requests.get(url + endpoint, stream=True)
        response.raise_for_status()
        data = []
        for line in response.iter_lines():
          if line:
            data.append(json.loads(line))
        return data
        print(f"Successfully fetched data from {url}{endpoint}.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON from the response.")

def post_data():
    try:
      data = get_data(url,endpoint)
      output = []
      for i in data:
        for id, details in i.items():
        entry = {"account_id":id,"donor_level":details.get("donor_level"),"l5_amounts":details.get("l5_amounts",[])}
        output.append(entry)
      with open('donations.json','w',encoding='utf-8') as f:
        for i in output:
          json.dump(i,f)
          f.write('\n')
          f.close()
          file_path = 'automated_load'
          file_name = 'donations.json'
          gcp_storage_client = storage.Client(storage_client)
          gcp_storage_bucket = gcp_storage_client.bucket(storage_bucket)
          file_upload = gcp_storage_bucket.blob(file_path + '/' + file_name)
          file_upload.upload_from_filename(file_name)    
          print(output)
    except:
      print("Error creating output.")
      raise
