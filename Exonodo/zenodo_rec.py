import requests
import json
from requests_html import HTMLSession
import pandas as pd
import requests


if __name__ == "__main__":
    response = requests.get('https://zenodo.org/api/records',
                            params={'communities':"exomol","size":20, 'access_token': '87EdGUa0eTuaYZMkc4PFrZnlyQrTDc3Eq2LnQKgXhyHs2UfhjHygqC3nH5YL'})

    print(response.json())
    with open('../Archive/rec_0904.json','w') as f:
        json.dump(response.json(), f)
        
    aa = response.json()
    tmp = dict()
    for item in aa['hits']['hits']:
        tmp[item['metadata']['title']] = {"doi":"\hyperlink{" + item['links']['doi'] + "}{" + item['links']['doi'] + "}" }
        
    tmp = pd.DataFrame(tmp)
    tmp.to_excel('../Archive/aa.xlsx')