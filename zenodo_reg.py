import requests
import json
from requests import status_codes
from requests_html import HTMLSession


def find_recommend(data:dict):
    res = []
    for item in data:
        if isinstance(data[item], dict):
            if data[item]['recommended']:
                res.append(item)
    if len(res) > 0:
        return res[0]
    else:
        return False


def remove_skipped_data(data:dict, *, skips:list=['Spectroscopic', 'Spectrum overview']):
    tmp = []
    for skip in skips:
        for item in data:
            if skip in item:
                tmp.append(item)
            else:
                pass
    for item in tmp:
        del data[item]
    return data


def zenodo_decoder(data:dict, *, skips:list=['Spectroscopic', 'Spectrum overview']):
    """
        data: dict()
            in root[molecule type][molecule][isotope][database][data]
        skips: [str] or []
    """
    # set.intersection could not be used here as the keys in skips
    # may be a subset of the keys in data
    data = remove_skipped_data(data, skips=skips)
    res = {'description': str(), 'reference': set(), 'files': list()}
    for item in data:
        if item == 'Definitions file':
            file_name = data[item]['url'].split('/')[-1]
            res['files'].append(file_name)
            res['description'] += 'Definitions file:<br>%s<br>' % file_name
        else:
            res['description'] += '<br>' + data[item]['description'] + ':<br>'
            for ref in data[item]['references']:
                res['reference'].add(ref)
            for file in data[item]['files']:
                file_name = file['file_name']
                res['files'].append(file_name)
                res['description'] += file_name + '<br>'
    return res


def zenodo_ini(token:str):
    headers = {"Content-Type": "application/json"}
    params = {'access_token': token}

    r = requests.post('https://zenodo.org/api/deposit/depositions',
                        params=params,
                        json={},
                        # Headers are not necessary here since "requests" automatically
                        # adds "Content-Type: application/json", because we're using
                        # the "json=" keyword argument
                        # headers=headers,
                        headers=headers)
    # r.status_code
    return r


def zenodo_filling(*, id:str, metadata:dict, token:str):
    url = 'https://zenodo.org/api/deposit/depositions/%s' % id
    r = requests.put(url,
                     params={'access_token': token},
                     data=json.dumps(metadata),
                     headers={"Content-Type": "application/json"})
    if r.status_code == 200:
        print('deposition id:{id} auto filling is successful'.format(id=id))
    else:
        print('response code:{response}, something wrong filling'.format(
            response=r.status_code))


def zenodo_uploading(*, bucket_url:str, files:list, path_root:str='', token:str):
    url = bucket_url
    for file in files:
        file_name = file
        if path_root == '':
            file_path = file
        elif isinstance(path_root, str):
            file_path = '/'.join([path_root, file])

        with open(file_path, "rb") as fp:
            r = requests.put(
                "%s/%s" % (bucket_url, file_name),
                data=fp,
                params={'access_token': token},
            )

    if r.status_code == 200:
        print('deposition id:{id} auto uploading is successful'.format(id=id))
    else:
        print('response code:{response}, something wrong uploading'.format(
            response=r.status_code))


ACCESS_TOKEN = 'Mitwo0cwfer47Lvx51CTawELNJt9OYknMfP5WOvmNvJcYspgo9dGYDQiEFlL'
info = json.load(open('Archive/data_AlH.json', 'r'))

data = info
path_root = 'sample_data/mnt/data/exomol/exomol3_data/'
# isotope = '26Al1H'
# folder = data[isotope]
# db = find_recommend(folder)
def zenodo_reg(data, *, token:str='', path_root:str):
    for cat in data:
        for molecule in data[cat]:
            for isotope in data[cat][molecule]:
                if isinstance(data[cat][molecule][isotope], str):
                    continue

                folder = data[cat][molecule][isotope]
                db = find_recommend(folder)
                path = path_root + '/'.join(folder[db]['url'].split('/')[-3::])

                res = zenodo_decoder(data=folder[db]['data'],
                        skips=['Spectroscopic', 'opacity', 'Spectrum overview'])
                r = zenodo_ini(token=token)
                bucket_url = r.json()["links"]["bucket"]
                id = r.json()['id']
                # tbc
                metadata = {
                    'metadata': {
                        'title': 'The {db} dataset for {isotope}'.format(db=db, isotope=isotope),
                        'upload_type': 'dataset',
                        'description': res['description'],
                        'creators': [{"name": "Jonathan Tennyson", "affiliation": "University College London"}],
                        # {"name": "Katy Chubb", "affiliation": "SRON Netherlands Institute for Space Research", "orcid": "0000-0002-4552-4559"}
                        'references': list(res['reference'])
                    }
                }

                zenodo_filling(id=id, metadata=metadata, token=token)
                zenodo_uploading(bucket_url=bucket_url,
                                files=res['files'], path_root=path, token=token)

zenodo_reg(data=data, token=ACCESS_TOKEN, path_root=path_root)