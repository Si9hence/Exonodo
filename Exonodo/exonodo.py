# to be compatible with package install and normal calling
try:
    from . import zenodo_reg
    from . import exomol_arc
    from . import zenodo_sup
except:
    import zenodo_reg
    import exomol_arc
    import zenodo_sup

import json
from typing import Union
from argparse import ArgumentParser

class exonodo:

    def __init__(self, *, token='', path_info='', path_root='', path_arc='', sub_set=[], config ='', field=[]):

        if path_info != '':
            self.data = json.load(open(path_info, 'r'))
        else:
            self.data = dict()
            
        self.token = token
        self.path_root = path_root
        self.sub_set = sub_set
        self.path_arc = path_arc
        self.field = field
        if config:
            self.run_config(config)
        return


    def set_token(self, token):
        self.token = token

    def set_path_root(self, path_root):
        self.path_root = path_root

    def set_path_info(self, path_info):
        self.path_info = path_info

    def set_sub_set(self, sub_set):
        self.set_sub_set = sub_set
        
    def register(self):
        # display molecules for registration
        zenodo_sup.molecule_display(data=self.data, flag=True)
        txt_tmp = 'The dataset of printed molecules will be registered \n' + \
            'press y to confirm \n'
        if input(txt_tmp) == 'y':
            zenodo_reg.zenodo_main(
                data=self.data, token=self.token, path_root=self.path_root, field=self.field)
        else:
            print('registration abolished')
    
    def archive(self):
        exomol_arc.get_data_main(subset=self.sub_set, path_save=self.path_arc)

    def del_unpublished(self, ids: Union[str, list] = 'all'):
        zenodo_sup.zenodo_del_unpublished(token=self.token, ids=ids)

    def run_config(self, path_config):
        config = json.load(open(path_config, 'r'))
        if config['option'] == 'reg':
            xx = exonodo(token=config['token'],
                        path_info=config['path_arc'],
                        path_root=config['path_data'],
                        field=config['field'])
            xx.del_unpublished()
            xx.register()
            return
        elif config['option'] == 'arc':
            xx = exonodo(sub_set=config['sub_set'],
                        path_arc=config['path_arc'])
            xx.archive()
            return
        return

def load_config(config:str):
    exonodo(config=config)

def process():
    """ 
    Function called when inputs are given from the command-line interface
    """
    parser = ArgumentParser(description="""The --config method is recommended \n
                            users are allowed to input option, token, sub_set, path_arc, path_data\n
                            for single calling\n
                            * show the condition when the arguments is complusory""")
    parser.print_help()
    parser.add_argument('--config', help='path of configuration file')
    parser.add_argument('--option', help='arc for collection; reg for registration')
    parser.add_argument('--token', help='token of Zenodo <str>, * if option == reg')
    parser.add_argument('--sub_set', help='subset of archived data; optional if option == arc')
    parser.add_argument('--path_arc', help='path to save archive .json; * if option == arc or reg')
    parser.add_argument('--path_data', help='path of exomol database; * if option == reg')
    args = parser.parse_args()
    
    args_dict = vars(args)
    if args_dict.get('config'):
        # config = json.load(open(args.config, 'r'))
        # if 'option' in config:
        #     args.option = config['option']
        # if 'token' in config:
        #     args.token = config['token']
        # if 'path_arc' in config:
        #     args.path_arc = config['path_arc']
        # if 'path_data' in config:
        #     args.path_data = config['path_data']
        # if 'sub_set' in config:
        #     args.sub_set = config['sub_set']
        xx = exonodo().run_config(args.config)
        return 
    if args.option == 'reg':
        xx = exonodo(token=args.token,
                    path_info=args.path_arc,
                    path_root=args.path_data)
        xx.del_unpublished()
        xx.register()
        return
    elif args.option == 'arc':
        xx = exonodo(sub_set=args.sub_set,
                    path_arc=args.path_arc)
        xx.archive()
        return
    return


if __name__ == '__main__':
    # xx = exonodo(token='87EdGUa0eTuaYZMkc4PFrZnlyQrTDc3Eq2LnQKgXhyHs2UfhjHygqC3nH5YL',
    #              path_info='../archive/data_26Al1H.json',
    #              path_root='../sample_data/mnt/data/exomol/exomol3_data/')

    # xx.del_unpublished()
    # xx.register()
    load_config('../sample/config_reg_mo.json')
    # try:
    #     process()
    # except:
    #     pass

