import requests
import json

def data_validation(path_json):
    """
    This function validate the archived json file by the exomol.all provided by ExoMol website
    """
    def extract_keyword(txt):
        # extract keywork from exomol.all
        return txt.split("#")[0].strip()
    
    def get_exomol_all():
        # get exomol.all from ExoMol website
        tmp = requests.get('https://exomol.com/db/exomol.all').text.split("\n")
        exomol_all = {}
        for idx, itm in enumerate(tmp):
            if "# Molecule chemical formula" in itm:
                molecule_tmp = extract_keyword(itm)
                exomol_all[molecule_tmp] = {}
            if "# Iso-slug" in itm:
                exomol_all[molecule_tmp][extract_keyword(itm).replace("-","")] = extract_keyword(tmp[idx+2])
        return exomol_all
    
    def reformat_json(data):
        # reformat exomol.all file and check it with json archived file
        res = dict()
        for cat in data:
            res[cat] = dict()
            for molecule in data[cat]:
                res[cat][molecule] = dict()
                for isotope in data[cat][molecule]:
                    if isinstance(data[cat][molecule][isotope], dict):
                        res[cat][molecule][isotope] = str()
                        for db in data[cat][molecule][isotope]:
                            if isinstance(data[cat][molecule][isotope][db], dict):
                                if data[cat][molecule][isotope][db]['recommended']:
                                    res[cat][molecule][isotope] = db
                                    break
        return res
    
    data = json.load(open(path_json, 'r'))
    data = reformat_json(data)
    exomol_all = get_exomol_all()
    check_rec = []
    # check whether the keyword matches each other
    for cat in data:
        for molecule in data[cat]:
            # print(molecule)
            for isotope in data[cat][molecule]:
                if data[cat][molecule][isotope] != '':
                    if data[cat][molecule][isotope] != exomol_all[molecule][isotope]:
                        check_rec.append([[cat,molecule,isotope]])
    if len(check_rec) == 0:
        print('the collected data, {path_json}, has been verified to be correct by exomol.all'.format(path_json=path_json))
    else:
        print("following molecules do not match with exomol.al")
        for item in check_rec:
            print(item)
    return check_rec
