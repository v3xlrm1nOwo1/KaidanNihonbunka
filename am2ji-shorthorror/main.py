import re
import os
import sys
import signal
import pickle
import requests
import argparse
from tqdm import tqdm
from bs4 import BeautifulSoup




def quit(signal_number, frame):
    print('Quit!')
    save()
    sys.exit()


def get_kaidankai(page_number: int):
    '''
        - Complite url with 'page_number'.
        - From url get all div with 'no-thumbitiran' class name and save divs in list.
        - From any div in 'div_list' get kaidan 'url' and 'name'.
        - And From kadan url get kaidan text.
        - And the last save 'kaidan name', 'kaidan txt', 'kaidan url' and 'page number' in dict and save dict in list.
    '''
    
    url = f'https://am2ji-shorthorror.com/page/{page_number}'
    req = requests.get(url=url)
    bs = BeautifulSoup(req.text, 'lxml')

    # get all list with 'no-thumbitiran' class name
    div_list = bs.find_all('div', {'class': 'no-thumbitiran'})

    # check list is not empty
    if div_list is None:
        return None
    
    
    kaidankai_list = []
    for kaidan_info in div_list:
        # from any div get 'list name' and 'list url'
        kaidan_name = kaidan_info.find('a').text 
        kaidan_url = kaidan_info.find('a')['href']

        # use url to go the kaidankai page
        kaidan_req = requests.get(url=kaidan_url)
        kaidan_bs = BeautifulSoup(kaidan_req.text, 'lxml')

        kaidan_txt = ''
        for div_tage in kaidan_bs.find_all('div', class_='mainbox'):
            for p in div_tage.select('p'):
                txt = p.get_text(strip=True, separator='\n')

                if re.findall(r'#\d+', txt):
                    break

                kaidan_txt += f'{txt}\n'


        result = {
            'name': kaidan_name.strip(),
            'kaidan': kaidan_txt.strip(),
            'url': kaidan_url.strip(), 
            'page_num': page_number,
        }

        kaidankai_list.append(result)
    
    return kaidankai_list


def save():
    print(f'save {len(kaidankai_list)} kaidankai')
    with open(args.output_file, 'wb') as f:
        pickle.dump(kaidankai_list, f)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start-page', type=int, default=1, help='number of start page')
    parser.add_argument('-e', '--end-page', type=int, default=67, help='number of end page')
    parser.add_argument('-o', '--output-file', type=str, default='am2ji-shorthorror_data.pkl', help='output file and ext')
    parser.add_argument('-c', '--last-time', action='store_true', help='continue from last time')
    args = parser.parse_args()
    print(args)


    kaidankai_list = []

    if args.last_time and os.path.exists(args.output_file):
        with open(args.output_file, 'rb') as f:
            kaidankai = pickle.load(f)
            args.start_page = kaidankai[-1]['page_num'] + 1

    for i in tqdm(range(args.start_page, args.end_page + 1)):
        kaidankai = get_kaidankai(page_number=i)

        if kaidankai is None:
            continue
        
        kaidankai_list += kaidankai
    
    save()

