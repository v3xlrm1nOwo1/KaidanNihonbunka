import re
import signal
import pickle
import requests
import argparse
from tqdm import tqdm
from bs4 import BeautifulSoup



def get_kaidankai_info(page_number: int):
    '''
        - To Complete url convert page_number to string and add more zeros to number depending on 'the length string number - 3'.
        - From url get main_tag and from it extract 'kaidan_name' and 'kaidan_txt'.
        - And the last save 'kaidan name', 'kaidan txt' and 'kaidan url' in dict.
    '''

    zeros = (3 - len(str(page_number))) * '0'
    page_number = zeros + str(page_number)
    
    url = f'http://hukumusume.com/douwa/pc/100monogatari/{page_number}.htm'
    
    req = requests.get(url=url)
    bs = BeautifulSoup(req.content, 'lxml')

    main_tag = bs.find('td', {'width': '619'})
    
    if main_tag is None:
        return None
    
    kaidan_name = main_tag.find('p', {'align': 'center'}).text
    kaidan_name = kaidan_name.split('\n')[-1].strip()
    try:
        html_string = main_tag.find_all('p')
        html_string = str(html_string[-3])

        pattern = re.compile(r'<.*?>')
        kaidan = pattern.sub('', html_string)
    except:
        kaidan = None
        print(url)

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
    parser.add_argument('-e', '--end-page', type=int, default=334, help='number of end page')
    parser.add_argument('-o', '--output-file', type=str, default='hukumusume_data.pkl', help='output file and ext')
    args = parser.parse_args()
    print(args)


    kaidankai_info_list = []
    for i in tqdm(range(args.start_page, args.end_page + 1)):

        kaidankai_info = get_kaidankai_info(page_number=i)

        if kaidankai_info is None:
            continue
        
        kaidankai_info_list.append(kaidankai_info)
    save()


