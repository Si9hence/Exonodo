from os import path
import zenodo_reg
import exomol_arc
import zenodo_sup
import json
from typing import Union
# info = {'token':'Mitwo0cwfer47Lvx51CTawELNJt9OYknMfP5WOvmNvJcYspgo9dGYDQiEFlL',}
# class info_group:
#     def __init__(self, info):
#         self.token = info['token']
#     # token = 'Mitwo0cwfer47Lvx51CTawELNJt9OYknMfP5WOvmNvJcYspgo9dGYDQiEFlL'
#     def set_token(self, token):
#         self.token = token


class exonodo:

    def __init__(self, *, token='', path_info='', path_root='') -> None:
        if token == '':
            print('please set a token if you want to reg on Zenodo ')
        self.token = token

        if path_info != '':
            self.data = json.load(open(path_info, 'r'))
        else:
            self.data = dict()

        if path_root != '':
            self.path_root = path_root

    def set_token(self, token):
        self.token = token

    def set_path_root(self, path_root):
        self.path_root = path_root

    def set_path_info(self, path_info):
        self.path_info = path_info

    def register(self):
        zenodo_sup.molecule_display(data=self.data, flag=True)
        txt_tmp = 'The dataset of printed molecules will be registered \n' + \
            'press y to confirm'
        if input(txt_tmp) == 'y':
            zenodo_reg.zenodo_main(
                data=self.data, token=self.token, path_root=self.path_root)
        else:
            print('registration abolished')

    def del_unpublished(self, ids: Union[str, list] = 'all'):
        zenodo_sup.zenodo_del_unpublished(token=self.token, ids=ids)


if __name__ == '__main__':
    xx = exonodo(token='87EdGUa0eTuaYZMkc4PFrZnlyQrTDc3Eq2LnQKgXhyHs2UfhjHygqC3nH5YL',
                 path_info='../archive/data_AlH.json',
                 path_root='../sample_data/mnt/data/exomol/exomol3_data/')

    xx.del_unpublished()
    xx.register()

# token = 'Mitwo0cwfer47Lvx51CTawELNJt9OYknMfP5WOvmNvJcYspgo9dGYDQiEFlL'
# data = json.load(open('../Archive/data_AlH.json', 'r'))

# path_root = '../sample_data/mnt/data/exomol/exomol3_data/'
# # isotope = '26Al1H'
# # folder = data[isotope]
# # db = find_recommend(folder)
# zenodo_reg(data=data, token=info['token'], path_root=path_root)
