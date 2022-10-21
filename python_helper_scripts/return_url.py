import os
import re 
import time
import lxml
import requests
import multiprocessing
from functools import partial
from bs4 import BeautifulSoup


BASE_GCE_URL = 'https://papers.gceguide.com/A%20Levels/'
def fetch_subject_list():
    subject_dict = {}
    r = requests.get(BASE_GCE_URL)
    soup = BeautifulSoup(r.text, 'lxml')
    
    for link in soup.find_all('a', class_='name'):
        
        sub_code = re.findall('\(([^)]+)\)',link.text)[-1]
        sub_name = link.text.split('(')[0]
        subject_dict.update({sub_name:sub_code})
    print(subject_dict)

