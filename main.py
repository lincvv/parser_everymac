import os
from urllib.parse import urlparse
from djparsing.core import Parser
from djparsing import data

files_path_mac = 'macbook'
url_mac = 'https://everymac.com/systems/apple/macbook/index-macbook.html'


class EveryMacPars(Parser):
    start_page = data.BodyCssSelect(start_url="span#contentcenter_specs_externalnav_2 > a", add_domain=True,
                                    body_count=50)
    name_file = data.ExtraDataField(save_start_url=True)
    table = data.TextContentCssSelect()
    text = data.TextContentCssSelect()


every_obj = EveryMacPars(url=url_mac,
                         start_page='div#wrapper',
                         text='div#contentcenter',
                         table='div#contentcenter_specs_table')


result = every_obj.run(create=False)

name_file = None
for data in result:
    if isinstance(data, int):
        name_file = F'{files_path_mac}\EveryMac_{data}.txt'

        continue

    if data.get('name_file', None):

        new_name_file = F"{files_path_mac}\{urlparse(data['name_file']).path.strip('.html').split('/')[-1]}.txt"
        if os.path.isfile(name_file) and new_name_file != name_file:
            os.rename(name_file, new_name_file)

        name_file = new_name_file

        with open(name_file, 'a+', encoding="utf-8") as f:
            f.write(F'\n\n\n{"#"*100}')
            f.write(data['name_file'])
            f.write(F'{"#"*100}\n\n\n')

        continue

    if data.get('table', None):
        with open(name_file, 'a+', encoding="utf-8") as f:
            f.write(data['table'])

        continue

    if data.get('text', None):
        with open(name_file, 'a+', encoding="utf-8") as f:
            f.write(data['text'])

        continue


