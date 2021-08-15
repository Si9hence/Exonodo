import requests
import json
# from requests_html import HTMLSession


url = 'https://zenodo.org/login/'
url_jenny = 'https://zenodo.org/deposit/5150278'
url_jenny2 = 'https://zenodo.org/api/deposit/depositions/5150278'

ACCESS_TOKEN = 'Mitwo0cwfer47Lvx51CTawELNJt9OYknMfP5WOvmNvJcYspgo9dGYDQiEFlL'


headers = {"Content-Type": "application/json"}
params = {'access_token': ACCESS_TOKEN}

r = requests.post('https://zenodo.org/api/deposit/depositions',
                   params=params,
                   json={},
                   # Headers are not necessary here since "requests" automatically
                   # adds "Content-Type: application/json", because we're using
                   # the "json=" keyword argument
                   # headers=headers,
                   headers=headers)
r.status_code
r.json()

bucket_url = r.json()["links"]["bucket"]

# New API
filename = "24Mg-1H__MoLLIST.R1000_0.3-50mu.ktable.ARCiS.fits.gz"
path = "C:/Users/Yulin/OneDrive/UCL/Course/Project/Jonathan/Code/sample/%s" % filename

# The target URL is a combination of the bucket link with the desired filename
# seperated by a slash.
with open(path, "rb") as fp:
    r = requests.put(
        "%s/%s" % (bucket_url, filename),
        data=fp,
        params=params,
    )
r.json()

data = {
    'metadata': {
        'title': 'My first upload',
        'upload_type': 'poster',
        'description': 'This is my first upload',
        'creators': [{'name': 'Doe, John',
                    'affiliation': 'Zenodo'}]
    }
}
deposition_id = r.json()["links"]

r = requests.put('https://zenodo.org/api/deposit/depositions/%s' % deposition_id,
                params={'access_token': ACCESS_TOKEN}, data=json.dumps(data),
                headers=headers)
r.status_code