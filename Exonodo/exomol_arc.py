from Exonodo.zenodo_sup import print_data
from os import path
from requests_html import HTMLSession
import requests
from time import sleep, strftime, localtime
import json

try:
    from .exomol_val import data_validation
except:
    from exomol_val import data_validation

def get_molecule(url:str):
    """
    The function accepts the Exomol molecule page url and returns an archive of the
    chemical formula of molecule and its url
    """
    s = HTMLSession()
    r = s.get(url)
    res = {}

    # div.grid-item is the HTML class of the molecule class
    for item in r.html.find(selector = 'div.grid-item'):
        res[item.text.split("\n")[0]] = {}
        tmp_links = list(item.links)
        tmp_abslinks = list(item.absolute_links)
        tmp_links.sort()
        tmp_abslinks.sort()
        for i in range(len(tmp_links)):
            # append the collected chemical formula and url link
            res[item.text.split("\n")[0]][tmp_links[i]]={'url':tmp_abslinks[i]}
    return res

def get_isotope(url):
    """
    The function accepts the isotopologue page url and returns an archive of the
    chemical formula of the isotopologue and its url
    """
    s = HTMLSession()
    r = s.get(url)
    # div.list-group is the HTML class of the molecule class
    tmp = r.html.find(selector = 'div.list-group')[0]
    tmp_text = tmp.text.split(' ')
    tmp_text.sort()
    tmp_abslinks = list(tmp.absolute_links)
    tmp_abslinks.sort()
    res = {}
    for i in range(len(tmp_text)):
        # append url
        res[tmp_text[i]] = {'url':tmp_abslinks[i]}
    return res

def get_dataset(url):
    """
    The function accepts the dataset page url and returns an archive of the
    dataset name and its url
    """
    s = HTMLSession()
    r = s.get(url)
    tmp = r.html.find(selector = 'div.list-group')[0].find(selector='a')
    res = {}
    # append the recommended keyword into res
    for item in tmp:
        if 'recommended' in item.attrs['class']:
            res[item.links.pop()] = {'url':item.absolute_links.pop(), 'recommended':True}
        else:
            res[item.links.pop()] = {'url':item.absolute_links.pop(), 'recommended':False}
    return res

def get_data_general(item):
    """
    The function accepts an HTML response and returns an reformatted data information
    of a general description of ExoMol files
    """
    label = item.find(selector='h4')[0].text
    description = item.find(selector='p')[0].text
    references = []
    # ol and li are HTML/CSS keywords to locate the reference
    for element in item.find(selector='ol')[0].find(selector='li'):
        tmp_ref = element.text
        if 'link to article' in tmp_ref:
            tmp_ref = tmp_ref.replace('link to article', element.absolute_links.pop())
        elif '\nurl:' in tmp_ref:
            tmp_ref = tmp_ref.replace('\nurl:', '[') + ']'
        else:
            print(tmp_ref)
        references.append(tmp_ref)
    
    files = []
    # li.list-group-item are HTML/CSS keywords to locate the file description and url
    for element in item.find(selector='li.list-group-item'):
        file_name = element.text.split('\n')[0].split(' ')[0]
        file_description = element.text.split('\n')[1]
        file_url = element.absolute_links.pop()
        files.append({'file_name':file_name,'description':file_description,'url':file_url})

    return {label:{'description':description, 'references':references, 'files':files}}

def get_data(url):
    """
    The function accepts an url and returns get data from different kinds for data files
    """    
    
    s = HTMLSession()
    r = s.get(url)
    tmp = r.html.find(selector = 'div.well')
    res = {}

    for item in tmp:
        # the definition file will be collected
        if 'Definitions file' in item.find(selector='h4')[0].text:
            for i in range(len(item.find(selector='h4'))):
                label = item.find(selector='h4')[i].text
                abs_links = item.find(selector='div.list-group')[i].absolute_links.pop()
                res[label] = {'url':abs_links}
        # the spectrum over file will be collected
        elif 'Spectrum overview' in item.find(selector='h4')[0].text:
            label = item.find(selector='h4')[0].text
            res[label] = {'url':item.find(selector="img")[0].attrs['src']}
        # other kinds of files will be collected using function get_data_general
        elif 'line list' in item.find(selector='h4')[0].text:
            res.update(get_data_general(item))
        elif 'partition function' in item.find(selector='h4')[0].text:
            res.update(get_data_general(item))
        elif 'opacity' in item.find(selector='h4')[0].text:
            res.update(get_data_general(item))
        # there are two cross section: abs cross section VUV cross section
        elif 'cross section' in item.find(selector='h4')[0].text:
            res.update(get_data_general(item))
        elif 'cooling function' in item.find(selector='h4')[0].text:
            res.update(get_data_general(item))
        elif 'other States files' in item.find(selector='h4')[0].text:
            res.update(get_data_general(item))
        elif 'heat capacity' in item.find(selector='h4')[0].text:
            res.update(get_data_general(item))    
        elif 'broadening coefficients' in item.find(selector='h4')[0].text:
            res.update(get_data_general(item))
        elif 'program' in item.find(selector='h4')[0].text:
            res.update(get_data_general(item))
        elif 'documentation' in item.find(selector='h4')[0].text:
            res.update(get_data_general(item))        
        elif 'super-line' in item.find(selector='h4')[0].text:
            res.update(get_data_general(item))
        elif 'ExoCross' in item.find(selector='h4')[0].text:
            res.update(get_data_general(item))
        
        else:
            print(item.find(selector='h4')[0].text)
    return res

def get_data_main(*, subset={'cat':[]}, path_save='./', valid = True):
    """
    subset: the molecule class to collect from ExoMol
    path_save: the folder to save the archived data
    
    Main function for collection process. The function accepts an
    the subset of molecule class which is required to collected
    and a path to save the file
    """
    url = 'https://exomol.com/data/molecules/'
    # get main molecule list first
    res = get_molecule(url)
    # cat stands for catalogy
    if not subset['cat']:
        subset['cat'] = res.keys()
    else:
        pass
    # add file names automatically by current time
    if path_save[-1] == '/':
        path_save = path_save + strftime("%y%m%d_%H%M%S", localtime()) + '.json'
    msg = '{cat} cat will be archived to {path_save}, press y to confirm'.format(cat=list(subset['cat']), 
                                                                                 path_save=path_save) 
    

    if input(msg) != 'y':
        print('archive abolished')
        return
    
    # cat for molecule catalogy
    for cat in subset['cat']:
        for molecule in res[cat]:
            # archive isotopologue information
            url = res[cat][molecule]['url']
            res[cat][molecule].update(get_isotope(url))
            # to avoid request limit
            sleep(4)
            for isotope in res[cat][molecule]:
                # archive dataset information
                if isinstance(res[cat][molecule][isotope], dict):
                    url = res[cat][molecule][isotope]['url']
                    res[cat][molecule][isotope].update(get_dataset(url))
                    print("collecting " + isotope)
                    sleep(4)
                    for dataset in res[cat][molecule][isotope]:
                        # archive data files information
                        if isinstance(res[cat][molecule][isotope][dataset], dict):
                            url = res[cat][molecule][isotope][dataset]['url']
                            res[cat][molecule][isotope][dataset]['data'] = get_data(url)
                            sleep(4)
                            print("db: " + dataset)
    # savefiles
    with open(path_save,'w') as f:
        json.dump(res, f)
    
    if valid:
        data_validation(path_save)
    return res


if __name__ == '__main__':
    # url = 'https://exomol.com/data/molecules/'
    # res = get_molecule(url)
    # cat = 'metal hydrides'
    # molecule = 'AlH'
    # for cat in res:
    #     for molecule in res[cat]:
    #         url = res[cat][molecule]['url']
    #         res[cat][molecule].update(get_isotope(url))
    #         sleep(4)
    #         for isotope in res[cat][molecule]:
    #             if isinstance(res[cat][molecule][isotope], dict):
    #                 url = res[cat][molecule][isotope]['url']
    #                 res[cat][molecule][isotope].update(get_dataset(url))
    #                 print(isotope)
    #                 sleep(4)
    #                 for dataset in res[cat][molecule][isotope]:
    #                     if isinstance(res[cat][molecule][isotope][dataset], dict):
    #                         url = res[cat][molecule][isotope][dataset]['url']
    #                         res[cat][molecule][isotope][dataset]['data'] = get_data(url)
    #                         sleep(4)
    #                         print(dataset)

    # with open('../Archive/data_all.json','w') as f:
    #     json.dump(res, f)
    # get_data_main(subset={'cat':['metal hydrides']}, path_save='../Archive/')
    
    data_validation("../Archive/data_metal.json")