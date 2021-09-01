from requests_html import HTMLSession
from time import sleep, time, strftime, localtime
import json
# url = 'https://exomol.com/data/molecules/'

def get_molecule(url):
    s = HTMLSession()
    r = s.get(url)
    res = {}
    for item in r.html.find(selector = 'div.grid-item'):
        res[item.text.split("\n")[0]] = {}
        tmp_links = list(item.links)
        tmp_abslinks = list(item.absolute_links)
        tmp_links.sort()
        tmp_abslinks.sort()
        for i in range(len(tmp_links)):
            res[item.text.split("\n")[0]][tmp_links[i]]={'url':tmp_abslinks[i]}
    return res

# res = get_molecule(url)

def get_isotope(url):
    s = HTMLSession()
    r = s.get(url)
    tmp = r.html.find(selector = 'div.list-group')[0]
    tmp_text = tmp.text.split(' ')
    tmp_text.sort()
    tmp_abslinks = list(tmp.absolute_links)
    tmp_abslinks.sort()
    res = {}
    for i in range(len(tmp_text)):
        res[tmp_text[i]] = {'url':tmp_abslinks[i]}
    return res

# url = 'https://exomol.com/data/molecules/MgH'

# for cat in res:
#     for molecule in res[cat]:
#         url = res[cat][molecule]['url']
#         res[cat][molecule].update(get_isotope(url))
#         sleep(4)
#     print(cat)

# url = 'https://exomol.com/data/molecules/MgH/24Mg-1H/'

def get_dataset(url):
    s = HTMLSession()
    r = s.get(url)
    tmp = r.html.find(selector = 'div.list-group')[0].find(selector='a')
    res = {}
    for item in tmp:
        if 'recommended' in item.attrs['class']:
            res[item.links.pop()] = {'url':item.absolute_links.pop(), 'recommended':True}
        else:
            res[item.links.pop()] = {'url':item.absolute_links.pop(), 'recommended':False}
    return res


# cat = 'metal hydrides'
# molecule = 'AlH'
# for cat in res:
#     for molecule in res[cat]:
#         for isotope in res[cat][molecule]:
#             if isinstance(res[cat][molecule][isotope], dict):
#                 url = res[cat][molecule][isotope]['url']
#                 res[cat][molecule][isotope].update(get_data_set(url))
#                 sleep(4)

def get_data_general(item):

    label = item.find(selector='h4')[0].text

    description = item.find(selector='p')[0].text

    references = []
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
    for element in item.find(selector='li.list-group-item'):
        file_name = element.text.split('\n')[0].split(' ')[0]
        file_description = element.text.split('\n')[1]
        file_url = element.absolute_links.pop()
        files.append({'file_name':file_name,'description':file_description,'url':file_url})

    return {label:{'description':description, 'references':references, 'files':files}}

# url = 'https://exomol.com/data/molecules/MgH/24Mg-1H/MoLLIST/'
url = 'https://exomol.com/data/molecules/AlH/27Al-1H/AlHambra/'
def get_data(url):
    s = HTMLSession()
    r = s.get(url)
    tmp = r.html.find(selector = 'div.well')
    res = {}
    # general_list = {'line list', 'partition function', 'opacity', 'cross section', 'cooling function', 'other States files'}

    for item in tmp:
        if 'Definitions file' in item.find(selector='h4')[0].text:
            for i in range(len(item.find(selector='h4'))):
                label = item.find(selector='h4')[i].text
                abs_links = item.find(selector='div.list-group')[i].absolute_links.pop()
                res[label] = {'url':abs_links}

        elif 'Spectrum overview' in item.find(selector='h4')[0].text:
            label = item.find(selector='h4')[0].text
            res[label] = {'url':item.find(selector="img")[0].attrs['src']}

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


def get_data_main(*, subset={'cat':[]}, path_save='./'):
    
    url = 'https://exomol.com/data/molecules/'
    res = get_molecule(url)
    if not subset['cat']:
        subset['cat'] = res.keys()
    else:
        pass
    if path_save[-1] == '/':
        path_save = path_save + strftime("%y%m%d_%H%M%S", localtime()) + '.json'
    msg = '{cat} cat will be archived to {path_save}, press y to confirm'.format(cat=list(subset['cat']), 
                                                                                 path_save=path_save) 
    

    if input(msg) != 'y':
        print('archive abolished')
        return
    
    for cat in subset['cat']:
        for molecule in res[cat]:
            url = res[cat][molecule]['url']
            res[cat][molecule].update(get_isotope(url))
            sleep(4)
            for isotope in res[cat][molecule]:
                if isinstance(res[cat][molecule][isotope], dict):
                    url = res[cat][molecule][isotope]['url']
                    res[cat][molecule][isotope].update(get_dataset(url))
                    print(isotope)
                    sleep(4)
                    for dataset in res[cat][molecule][isotope]:
                        if isinstance(res[cat][molecule][isotope][dataset], dict):
                            url = res[cat][molecule][isotope][dataset]['url']
                            res[cat][molecule][isotope][dataset]['data'] = get_data(url)
                            sleep(4)
                            print(dataset)
    with open(path_save,'w') as f:
        json.dump(res, f)
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
    get_data_main(subset={'cat':['metal hydrides']}, path_save='../Archive/')