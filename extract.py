import requests
import lxml.html
import argparse
from urllib.parse import urlparse


class gdriveFolder(object):
    def __init__(self, id):
        self.id = id
        self.source = None
        self.source_xml = None
        self.title = False
        self.urls = []
        self.get_page()
    def get_page(self):
        url = f'https://drive.google.com/drive/folders/{id}'
        try:
            r = requests.get(url)
            if r.status_code != 200:
                raise Exception(f'Status code != 200 getting details from folder ID {id}')
            xml = lxml.html.fromstring(r.text)
            self.source_xml = xml
            self.get_title()
        except Exception as err:
            raise Exception(err)
    def is_available(self):
        if self.source_xml is not None:
            return True
        else:
            raise Exception('No source available')
        return True if self.source_xml else False
    def get_title(self):
        if self.is_available():
            try:
                title_elem = self.source_xml.xpath('//title')
                if len(title_elem)>=1:
                    self.title = title_elem[0].text_content().strip()
            except Exception as err:
                raise Exception(err)
    def get_url_files(self):
        if self.is_available():
            try:
                url_elem = self.source_xml.xpath('//*[@data-id]')
                for elem in url_elem:
                    url_final = f'https://drive.google.com/file/d/{elem.attrib["data-id"]}/view?usp=sharing'
                    self.urls.append(url_final)
                return True
            except Exception as err:
                raise Exception(err)
        return False



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', type=str, required=False, help='ID GoogleDrive Folder')
    parser.add_argument('--url', type=str, required=False, help='URL GoogleDrive Folder')
    args = parser.parse_args()
    if not args.id:
        data_parse = urlparse(args.url)
        if data_parse.path.startswith('/drive/folders/') == False:
            raise Exception(f'Invalid URL {args.url}')
        id = data_parse.path.split('/')[3].strip()
    else:
        id = args.id
    g_inst = gdriveFolder(id)
    if g_inst.get_url_files():
        print(f'{g_inst.title}\tTotal Files {len(g_inst.urls)}\n\n')
        for url in g_inst.urls:
            print(url)


