import requests
import json
import csv
# from requests import status_codes
# from requests_html import HTMLSession


def find_recommend(data: dict):

    def find_prime(res):
        prime = ['MoLLIST']
        for db in res:
            if db in prime:
                return db
        return False

    res = []
    for item in data:
        if isinstance(data[item], dict):
            if data[item]['recommended']:
                res.append(item)
    
    if len(res) > 0:
        if find_prime(res):
            return find_prime(res)
        else:
            return res[0]
    else:
        return False


def remove_skipped_data(data: dict, *, skips: list = ['Spectroscopic', 'Spectrum overview']):
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


def keep_kept_data(data: dict, *,
                   keeps: list = ['Definitions file', 'line list', 'partition function', 'opacity']):
    tmp = []
    for keep in keeps:
        for item in data:
            if keep in data:
                tmp.append(item)
            else:
                pass

    for item in data:
        if item not in tmp:
            del data[item]
    return data


def zenodo_decoder(data: dict, *,
                   skips: list = ['Spectroscopic',
                                  'Spectrum overview'],
                   keeps: list = ['Definitions file',
                                  'line list',
                                  'partition function',
                                  'opacity']):
    """
        data: dict()
            in root[molecule type][molecule][isotope][database][data]
        skips: [str] or []
    """
    url = data['url']
    data = data['data']

    def insert_space(n=1):
        return '&nbsp;'*n
    # set.intersection could not be used here as the keys in skips
    # may be a subset of the keys in data
    data = remove_skipped_data(data, skips=skips)
    data = keep_kept_data(data, keeps=keeps)

    reference_base = """J. Tennyson, S.N. Yurchenko A.F. Al-Refaie, V.H.J. Clark, K.L. Chubb,E.K. Conway, A. Dewan, M.N. Gorman, C. Hill, A.E. Lynas-Gray, T. Mellor, L.K. McKemmish, A. Owens, O.L. Polyansky, M. Semenov, W. Somogyi, G. Tinetti, A. Upadhyay, I. Waldmann, Y. Wang, S. Wright and O.P. Yurchenko, The 2020 release of the ExoMol database: molecular line lists for exoplanet and other hot atmospheres, J. Quant. Spectrosc. Rad. Transf., 255, 107228 (2020).[https://doi.org/10.1016/j.jqsrt.2020.107228.]"""
    reference_ExoMol = "Root references for ExoMol database: <br>{space}1. {ref}<br>".format(
        space=insert_space(n=2), ref=reference_base)
    descrption_ini = 'The dataset is an archive of ExoMol page, {url}.<br> Please check the reference details according to the following description or directly from the website.<br><br>'.format(
        url=url)
    res = {'description': descrption_ini,
           'reference': set([reference_base]),
           'files': list()}
    for item in data:
        if item == 'Definitions file':
            file_name = data[item]['url'].split('/')[-1]
            res['files'].append(file_name)
            res['description'] += 'Definitions file:<br>%s<br>' % file_name
            res['description'] += reference_ExoMol
        else:
            
            res['description'] += '<br>{title}<br>{des}:<br>'.format(
                title=item, des=data[item]['description'])
            for cnt, file in enumerate(data[item]['files']):
                file_name = file['file_name']
                res['files'].append(file_name)
                res['description'] += '{space}{file_name}<br>'.format(
                    space=insert_space(n=2), file_name=file_name)
                res['description'] += '{space}{des}<br>'.format(
                    space=insert_space(n=4), des=file['description'])
                # if cnt == len(data[item]['files'])-1:
                #     res['description'] += '<br>'
            res['description'] += 'References:<br>'
            for numbering, ref in enumerate(data[item]['references']):
                res['reference'].add(ref)
                res['description'] += "{space}{numbering}. {ref}<br>".format(
                    space=insert_space(n=2), numbering=numbering+1, ref=ref)
    return res


def zenodo_ini(token: str):
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


def zenodo_fill(*, deposit_id: str, metadata: dict, token: str):
    url = 'https://zenodo.org/api/deposit/depositions/%s' % deposit_id
    r = requests.put(url,
                     params={'access_token': token},
                     data=json.dumps(metadata),
                     headers={"Content-Type": "application/json"})
    if r.status_code == 200:
        print('deposition id:{deposit_id} auto filling is successful'.format(
            deposit_id=deposit_id))
    else:
        print('response code:{response}, something wrong filling'.format(
            response=r.status_code))


def zenodo_upload(*, deposit_id: str, bucket_url: str, files: list, path_root: str = '', token: str):
    for file in files:
        file_name = file
        if path_root == '':
            file_path = file
        elif isinstance(path_root, str):
            file_path = '/'.join([path_root, file])
        try:
            with open(file_path, "rb") as fp:
                r = requests.put(
                    "%s/%s" % (bucket_url, file_name),
                    data=fp,
                    params={'access_token': token},
                )
        except:
            print(file_path + 'does not exist in the directory')

    if r.status_code == 200:
        print('deposition id:{deposit_id} auto uploading is successful'.format(
            deposit_id=deposit_id))
    else:
        print('response code:{response}, something wrong uploading'.format(
            response=r.status_code))


def zenodo_metadata(*, data: dict, res: dict, db: str, isotope: str, path_file: str):
    
    def search_version(path_def):
        info = csv.reader(open(path_def, 'r'))
        for item in info:
            if 'Version number' in item[0]:
                return item[0].split(' ')[0]

    def match_creators(res):
    
        creators_info = {
            "Tennyson, J.": {"affiliation": "University College London",
                             "orcid": "0000-0002-4994-5238"},
            "Yurchenko, S. N.": {"affiliation": "University College London",
                                 "orcid": "0000-0001-9286-9501"},
            "Williams, H.": {"affiliation": "University College London"},
            "Victoria H. J. Clark": {"affiliation": "University College London",
                                     "orcid": "0000-0002-4384-2625"},
            "Leyland, P. C.": {"affiliation": "University College London"},
            "Chubb, K. L.": {"affiliation": "SRON Netherlands Institute for Space Research",
                             "orcid": "0000-0002-4552-4559"},
            "Lodi, L.": {"affiliation": "University College London"},
            "Rocchetto, M.": {"affiliation": "University College London"},
            "Waldmann, I.": {"affiliation": "University College London"},
            "Barstow, J. K.": {"affiliation": "University College London"},
            "Al-Refaie, A. F": {"affiliation": "University College London"},
            "Molliere, P.": {"affiliation": "Max Planck Institute for Astronomy"}
        }
        creators = []
        tmp = []
        for ref in list(res['reference']):
            if "[https://doi.org/10.1016/j.jqsrt.2020.107228.]" in ref:
                pass
            else:
                tmp = list(map(str.strip, ref.split("\"")[0].split(',')[:-1]))
            for item in [", ".join(item) for item in zip(tmp[0::2], tmp[1::2])]:
                if item not in creators:
                    creators.append(item)
            # creators.update(set(", ".join(item) for item in zip(tmp[0::2], tmp[1::2])))
        creators_meta = list()
        for creator in creators:
            creators_meta.append({'name':creator})
            if creator in creators_info:
                creators_meta[-1].update(creators_info[creator])
            else:
                pass
        return creators_meta
    
    def match_keywords(data):
        keywords = ["ExoMol"]
        for key in data['data']:
            if 'opacity' in key:
                keywords += ['Opacity', 'ExoMolOP']
            elif 'line list' in key:
                keywords += ['line list']
            elif 'partition function' in key:
                keywords += ['partition function']
        return keywords

    def match_grants(data):
        grants = []
        for key in data['data']:
            if 'opacity' in key:
                grants += [{"id": "10.13039/501100000780::776403"}]
            elif 'line list' or 'partition function' in key:
                grants += [{"id": "10.13039/501100000780::883830"}, {"id": "267219"}, {"id": "10.13039/501100000690::ST/R000476/1"}]
        return grants
    path_def = '/'.join([path_file,
                         [item for item in res['files'] if '.def' in item][0]])
    
    version = search_version(path_def)
    creators = match_creators(res)
    publication_date = '-'.join([version[0:4], version[4:6], version[6::]])
    keywords = match_keywords(data)
    grants = match_grants(data)
    references = list(res['reference'])
    description = res['description']
    metadata = {
        'metadata': {
            'title': 'The {db} dataset for {isotope}'.format(db=db, isotope=isotope),
            'upload_type': 'dataset',
            'description': description,
            'creators': creators,
            'references': references,
            'license': "CC-BY-4.0",
            'publication_date': publication_date,
            'access_right': "open",
            'communities': [{'identifier': "exomol"}],
            'keywords': keywords,
            'version': version,
            'grants': grants
        }
    }

    return metadata


def zenodo_main(data: dict, *, token: str = '', path_root: str):
    for cat in data:
        for molecule in data[cat]:
            for isotope in data[cat][molecule]:
                if isinstance(data[cat][molecule][isotope], str):
                    continue

                isot = data[cat][molecule][isotope]
                db = find_recommend(isot)
                if db is False:
                    print('no recommended db found, {isotope}skipped'.format(isotope=isotope))
                path_file = path_root + \
                    '/'.join(isot[db]['url'].split('/')[-3::])

                res = zenodo_decoder(data=isot[db],
                                     skips=['Spectroscopic', 'Spectrum overview'])
                r = zenodo_ini(token=token)
                bucket_url = r.json()["links"]["bucket"]
                deposit_id = r.json()['id']
                # tbc
                metadata = zenodo_metadata(
                    data=isot[db], res=res, db=db, isotope=isotope, path_file=path_file)

                zenodo_fill(deposit_id=deposit_id,
                            metadata=metadata, token=token)
                zenodo_upload(deposit_id=deposit_id, bucket_url=bucket_url,
                              files=res['files'], path_root=path_file, token=token)


if __name__ == '__main__':

    ACCESS_TOKEN = 'Mitwo0cwfer47Lvx51CTawELNJt9OYknMfP5WOvmNvJcYspgo9dGYDQiEFlL'
    info = json.load(open('../Archive/data_AlH.json', 'r'))
    pf = "C:\\Users\\Yulin\\OneDrive\\UCL\\Course\\Project\\Jonathan\\Exonodo\\sample_data\\mnt\\data\\exomol\\exomol3_data\\AlH\\26Al-1H\\AlHambra"
    path_root = '../sample_data/mnt/data/exomol/exomol3_data/'
    cat = 'metal hydrides'
    molecule = 'AlH'
    isotope = '26Al1H'
    db = find_recommend(info[cat][molecule][isotope])
    data = info[cat][molecule][isotope][db]

    info = json.load(open('../Archive/data_26Al1H.json', 'r'))
    res = zenodo_decoder(data)
    md = zenodo_metadata(data=data, res=res, db=db, isotope=isotope, path_file=pf)
    # zenodo_main(data=info, token=ACCESS_TOKEN, path_root=path_root)
