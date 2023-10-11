import requests
from requests.auth import HTTPBasicAuth

url = "https://demo.credy.in/api/v1/maya/movies/"
basic_auth = HTTPBasicAuth('iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0', 'Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', 
    "Upgrade-Insecure-Requests": "1",
    "DNT": "1",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate"
}
response = requests.request("GET", url, headers=headers, verify=False, auth=basic_auth)
all_movies_json =  response.text
print(all_movies_json)