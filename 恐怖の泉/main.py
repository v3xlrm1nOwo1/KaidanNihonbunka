import re
import signal
import pickle
import requests
import argparse
from tqdm import tqdm
from bs4 import BeautifulSoup



def get_kaidankai_info(page_number: int):
    '''
        - To Complete url get page_number.
        - From url get main_div and from it extract 'kaidan_name' and 'kaidan_txt'.
        - And the last save 'kaidan name', 'kaidan txt' and 'kaidan url' in dict.
    '''
    
    url = f'https://xn--u9jv84l7ea468b.com/kaidan/{page_number}wa.html' # 1wa.html , 2wa.html
    req = requests.get(url=url)
    bs = BeautifulSoup(req.content, 'lxml')

    main_div = bs.find('div', attrs={'class': 'main'})

    if main_div is None:
        return None
    
    kaidan_name = main_div.find('h1', attrs={'class': 'midashi2'})
    kaidan_name = kaidan_name.get_text().strip()


    html_string_list = main_div.find_all('p', attrs={'class': 'bun'})
    
    kaidan = ''
    for tag in html_string_list:
        pattern = re.compile(r'<.*?>')
        tag = pattern.sub('', str(tag))
        kaidan += f'{tag}\n'

    kaidan = kaidan.strip()

    result = {
        'kaidan': kaidan,
        'name': kaidan_name,
        'url': url,
        }

    return result


def save():
    print(f'save {len(kaidankai_info_list)} kaidankai')
    with open(args.output_file, 'wb') as f:
        pickle.dump(kaidankai_info_list, f)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start-page', type=int, default=1, help='number of start page')
    parser.add_argument('-e', '--end-page', type=int, default=744, help='number of end page')
    parser.add_argument('-o', '--output-file', type=str, default='恐怖の泉_data.pkl', help='output file and ext')
    args = parser.parse_args()
    print(args)


    kaidankai_info_list = []
    for i in tqdm(range(args.start_page, args.end_page + 1)):

        kaidankai_info = get_kaidankai_info(page_number=i)

        if kaidankai_info is None:
            continue
        
        kaidankai_info_list.append(kaidankai_info)
    save()


