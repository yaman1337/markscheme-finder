import os
import time
import lxml
import requests
import multiprocessing
from functools import partial
from bs4 import BeautifulSoup

SUBJECT = {
    'CHEMISTRY': 'https://papers.gceguide.com/A%20Levels/Chemistry%20(9701)/',
    'PHYSICS':   'https://papers.gceguide.com/A%20Levels/Physics%20(9702)/',
    'MATH':      'https://papers.gceguide.com/A%20Levels/Mathematics%20(9709)/',
    'COMPUTER':  'https://papers.gceguide.com/A%20Levels/Computer%20Science%20(for%20first%20examination%20in%202021)%20(9618)/',
    'EGP':       'https://papers.gceguide.com/A%20Levels/English%20General%20Paper%20(AS%20Level%20only)%20(8021)/',
    'F-MATH':    'https://papers.gceguide.com/A%20Levels/Mathematics%20-%20Further%20(9231)/'
}

PAPER_TERMS = {
    'qp':'QP',
    'ir':'IR',
    'ms':'MS',
    'er':'ER'
}
MAIN_DIR = os.getcwd()

def make_folder(Year,folder_name, dir_name:None):
    time.sleep(0.5)
    if dir_name is not None:
        os.chdir(dir_name)
    else:
        os.chdir(MAIN_DIR)
    if not os.path.exists(key):
        os.mkdir(key)
    else:
        os.chdir(key)
        if not os.path.exists(Year):   
            os.chdir(os.getcwd())
            os.mkdir(Year)
            os.chdir(Year)
        else:
            os.chdir(Year)
            if not os.path.exists(folder_name):
                os.mkdir(PAPER_TERMS[f'{folder_name}'])
                os.chdir(PAPER_TERMS[f'{folder_name}'])
            else:    
                os.chdir(PAPER_TERMS[f'{folder_name}'])
    return os.getcwd()

def downloader(PDF_NAME, PDF_LINK):
    try:
        with open(PDF_NAME, 'r') as pdf:
            print('File is already there')
            return 1
    except FileNotFoundError:
        print('New PDF')
        with open(PDF_NAME, 'wb') as pdf:
            r = requests.get(PDF_LINK)
            pdf.write(r.content)
            print('Downloaded')
            return 0
    except Exception:
        print('Cannot download the PDF {}'.format(PDF_NAME))

def main():
    global key
    for key, value in SUBJECT.items():
        
        r = requests.get(value)
        soup = BeautifulSoup(r.text, 'lxml')
        for link in soup.find_all('a', class_='name'):
            global Year
            Year = link.get('href')
            Year = Year.split('/')[-1]
            
            NEWURL = value + Year
            #print(NEWURL)
            r = requests.get(NEWURL)
            soup = BeautifulSoup(r.text, 'lxml')
            for link in soup.find_all('a', class_='name'):
                pdf_data = []
                PDF_NAME =  link.get('href')
                PDF_LINK = NEWURL + '/'+ link.get('href')
                pdf_data.append(PDF_NAME)
                for type in PAPER_TERMS:
                    if type in PDF_NAME:
                        folder_path = make_folder(Year, type)
                        with multiprocessing.Pool() as pool:
                            results = pool.map(
                                partial(downloader, PDF_LINK= PDF_LINK),pdf_data
                            )
if __name__ == '__main__':
	main()