from typing import Union
import requests
import json
from typing import Union
from time import sleep
from pprint import pprint
import zenodo_reg
# from requests import status_codes
# from requests_html import HTMLSession

ACCESS_TOKEN = 'Mitwo0cwfer47Lvx51CTawELNJt9OYknMfP5WOvmNvJcYspgo9dGYDQiEFlL'

r = requests.get('https://zenodo.org/api/deposit/depositions',
                 params={'access_token': ACCESS_TOKEN})


def zenodo_del_unpublished(token, *, ids: Union[str, list]):
    def del_check(res):
        if res.status_code == 204:
            print('del %s success' % id)
        elif res.status_code == 404:
            print('Deposition file does not exist')
        elif res.statis_code == 403:
            print('Deleting an already published deposition')

    def ids_list_gen(ids):
        ids_list = list()
        if ids == 'all':
            if input('clear all unpublished registration? y/n') == 'y':
                r = requests.get('https://zenodo.org/api/deposit/depositions',
                                 params={'access_token': token}).json()
                for item in r:
                    ids_list.append(item['id'])
            else:
                print('del abolished')
        elif isinstance(ids, str):
            ids_list = [ids]
        elif isinstance(ids, list) and len(ids) > 0:
            ids_list = ids
        return ids_list

    ids_list = ids_list_gen(ids)
    for id in ids_list:
        r = requests.delete('https://zenodo.org/api/deposit/depositions/%s' % id,
                            params={'access_token': token})
        del_check(r)
        sleep(1)


def molecule_display(data, flag=False):
    res = dict()
    for cat in data:
        res[cat] = dict()
        for molecule in data[cat]:
            res[cat][molecule] = dict()
            if isinstance(data[cat][molecule], dict):
                for isotope in data[cat][molecule]:
                    if isinstance(data[cat][molecule][isotope], dict):
                        res[cat][molecule][isotope] = ''
    if flag:
        for cat in res:
            print(cat)
            for molecule in res[cat]:
                print('    ' + molecule)
                tmp = []
                for isotope in res[cat][molecule]:
                    tmp.append(isotope)
                print('    '*2 + ";".join(tmp))
        return
    return res


def recommend_analysis(data):
    res = dict()
    for cat in data:
        res[cat] = dict()
        for molecule in data[cat]:
            res[cat][molecule] = dict()
            for isotope in data[cat][molecule]:
                if isinstance(data[cat][molecule][isotope], dict):
                    tmp = []
                    for db in data[cat][molecule][isotope]:
                        if isinstance(data[cat][molecule][isotope][db], dict):
                            if data[cat][molecule][isotope][db]['recommended']:
                                tmp.append(db)
                    res[cat][molecule][isotope] = zenodo_reg.find_recommend(data[cat][molecule][isotope])
    return res

def print_data(data):
    res = dict()
    for cat in data:
        res[cat] = dict()
        for molecule in data[cat]:
            res[cat][molecule] = dict()
            for isotope in data[cat][molecule]:
                if isinstance(data[cat][molecule][isotope], dict):
                    res[cat][molecule][isotope] = dict()
                    for db in data[cat][molecule][isotope]:
                        if isinstance(data[cat][molecule][isotope][db], dict):
                            if data[cat][molecule][isotope][db]['recommended']:
                                res[cat][molecule][isotope][db] = []
                                res[cat][molecule][isotope][db] = list(data[cat][molecule][isotope][db]['data'].keys())
    return res


if __name__ == '__main__':
    info = json.load(open('../Archive/data_metal copy.json', 'r'))
    res = recommend_analysis(info)
    # data = info
    # path_root = '../sample_data/mnt/data/exomol/exomol3_data/'
    # # isotope = '26Al1H'
    # # folder = data[isotope]
    # # db = find_recommend(folder)
