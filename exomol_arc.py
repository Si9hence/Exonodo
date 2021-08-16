from requests_html import HTMLSession
from time import sleep

url = 'https://exomol.com/data/molecules/'

def get_cat(url):
    s = HTMLSession()
    r = s.get(url)
    res = {}
    for item in r.html.find(selector = 'div.grid-item'):
        res[item.text.split("\n")[0]] = []
        tmp_links = list(item.links)
        tmp_abslinks = list(item.absolute_links)
        tmp_links.sort()
        tmp_abslinks.sort()
        tmp = zip(tmp_links, tmp_abslinks)
        for element in tmp:
            res[item.text.split("\n")[0]].append({'molecule':element[0], 'data':{}, 'url':element[1]})
    return res

res = get_cat(url)

def get_isotope(url):
    s = HTMLSession()
    r = s.get(url)
    tmp = r.html.find(selector = 'div.list-group')[0]
    tmp_text = tmp.text.split(' ')
    tmp_text.sort()
    tmp_abslinks = list(tmp.absolute_links)
    tmp_abslinks.sort()
    res = []
    for i in range(len(tmp_text)):
        res.append([{tmp_text[i]:''}, tmp_abslinks[i]])
    return res

url = 'https://exomol.com/data/molecules/MgH'

for item in res.keys():
    for element in res[item]:
        url = element['url']
        for key in element[0]:
            element[0][key] = get_isotope(url)
        sleep(5)
    print(item)

url = 'https://exomol.com/data/molecules/MgH/24Mg-1H/'

def get_data_set(url):
    s = HTMLSession()
    r = s.get(url)
    tmp = r.html.find(selector = 'div.list-group')[0].find(selector='a',containing='recommended')
    res = []
    for item in tmp:
        res.append([{item.links.pop():[]}, item.absolute_links.pop()])
    return res

for cat in res.keys():
    # res[cat] is [[{mole:[...]}, url], ...]
    for mole in res[cat]:
        for isot in mole[0]:
            for element in mole[0][isot]:
                url = element[1]
                tmp = get_data_set(url)
                for key in element[0].keys():
                    element[0][key] = tmp
            # url = isot[1]
            # tmp = get_data_set(url)
                sleep(5)

res = get_data_set(url)

url = 'https://exomol.com/data/molecules/MgH/24Mg-1H/MoLLIST/'
def get_data(url):
    s = HTMLSession()
    r = s.get(url)
    tmp = r.html.find(selector = 'div.well')
    res = []
    for item in tmp:
        if 'Definitions file' in item.find(selector='h4')[0].text:
            tmp_def = item.find(selector='div.list-group')
            for element in temp_def:
                res.append
        elif 'Spectrum overview' in item.find(selector='h4')[0].text:
            pass
        elif 'line list' in item.find(selector='h4')[0].text:
            pass
        elif 'partition function' in item.find(selector='h4')[0].text:
            pass
        elif 'opacity' in item.find(selector='h4')[0].text:
            pass
def get_data_def(item):
    tmp_def = item.find(selector='div.list-group')



# typeList = list()
# for item in r.html.absolute_links:
#   if "/data/data-types/" in item:
#     if item.split('/')[-2] == 'data-types' and item.split('/')[-1] != '':
#       typeList.append(item)

# typeSelect = 'opacity'

# for item in typeList:
#   res = list()
#   if typeSelect in item:
#     urlTmp = item
#     print('url = {urlTmp}'.format(urlTmp=urlTmp))
#     break


# moleList = list()
# for item in r.html.absolute_links:
#   if "/data/data-types/" in item:
#     if item.split('/')[-2] == 'data-types' and item.split('/')[-1] != '':
#       moleList.append(item)

# session = HTMLSession()
# tt = session.get('https://exomol.com/data/data-types/opacity/MgH/24Mg-1H/MoLLIST/')

# u = 'https://exomol.com/db/MgH/24Mg-1H/MoLLIST/24Mg-1H__MoLLIST.R1000_0.3-50mu.ktable.ARCiS.fits.gz'

# def download_file(url):
#     local_filename = url.split('/')[-1]
#     # stream=True to transfer the data
#     with requests.get(url, stream=True) as r:
#         r.raise_for_status()
#         with open(local_filename, 'wb') as f:
#             for chunk in r.iter_content(chunk_size=8192): 
#                 # If you have chunk encoded response uncomment if
#                 # and set chunk_size parameter to None.
#                 #if chunk: 
#                 f.write(chunk)
#     return local_filename

# download_file(u)