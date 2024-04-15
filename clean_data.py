import os
import g4f
import pickle
from tqdm import tqdm



def get_files_path(main_path: str):
    count = 0
    files_info = []

    for dir in os.listdir(main_path):
        dir = f'{main_path}/{dir}'
        try:
            for file in os.listdir(dir):
                if file.endswith('.pkl') and 'clean' not in file and 'idx' in file:
                    full_path = os.path.join(dir, file)
                    with open(full_path, 'rb') as f:
                        kaidankai = pickle.load(f)
                        count += len(kaidankai)
                        print(f'{file}: {len(kaidankai)}')
                        files_info.append(full_path)
        except:
            continue

    print(f'Total count: {count}')
    return files_info


def get_kaidan_name(name: str, kaidan: str):
    content = f'''Do you know the Japanese ghost stories Hyakumonogatari kaidankai?
I'll give you one of them and the name of the story, but there's a problem.
The name of the story contains text that I do not want like "【怖い話】" or other. It may be a name that contains unnecessary text or a bad name.
you need Clean the name from unnecessary texts, and if it needs to be modified, modify the name according to the content of the story well. 

- Note: Just rename the story you edited in Japanese, and write nothing else.  The name is understandable, I'm counting on you and good luck
name: {name}
kaidan: {kaidan}'''
    
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4_turbo,
        messages=[{
            'role': 'user', 
            'content': content,
        }],
        timeout=300,  # in secs
    )

    return response, name


if __name__ == '__main__':
    files = get_files_path(main_path = r'C:\Users\v3xlrm1nOwo1\Documents\Projects\Self Projects\Hyakumonogatari-Dataset')
    print(files)

    # loop over all not clean files
    for file in files:
        output_file = f'{file[: -4]}_clean.pkl'

        # open file
        with open(file, 'rb') as f:
            kaidankai = pickle.load(f)

        if os.path.exists(output_file):
            with open(output_file, 'rb') as f:
                clean_kaidankai = pickle.load(f)
                print(len(clean_kaidankai))
        else:
            clean_kaidankai = [{'index': 999999999999999999}]
        
        # loop over all data in file
        for kaidan in tqdm(kaidankai):
            if not (kaidan['index'] in [i['index'] for i in clean_kaidankai]):
                # get clean name and old name
                new_name, old_name = get_kaidan_name(name=kaidan['name'], kaidan=kaidan['kaidan'])
                # save data in dict
                result = {
                    'old name': old_name,
                    'new name': new_name,
                    **kaidan
                }

                # save dict in list
                clean_kaidankai.append(result)
                with open(output_file, 'wb') as f:
                    pickle.dump(clean_kaidankai, f)
            
        

        # save clean data in file
        print(f'save {len(clean_kaidankai)} kaidankai')

        with open(output_file, 'wb') as f:
            pickle.dump(clean_kaidankai, f)

