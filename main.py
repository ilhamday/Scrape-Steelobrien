import requests
from bs4 import BeautifulSoup
import json, glob
import pandas as pd
import time

def check_url_status():

    print('Check URL Status')

    urls = 'https://www.steelobrien.com/products'

    res = requests.get(urls, headers={'User-Agent': 'Mozilla/5.0'})

    print(res.status_code)

    print('Checking status complete!')

def get_urls_all_item():
    print(f'Getting all urls...')

    res = requests.get('https://www.steelobrien.com/products', headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(res.text, 'html.parser')

    titles  = soup.find_all('div', class_='col col-xs-12 col-sm-6 col-md-4')

    urls = []

    for title in titles:
        url = title.find('a')['href']
        url = 'https://www.steelobrien.com' + url
        print(url)
        urls.append(url)
        time.sleep(2)

    return urls

def get_second_level_url(url):
    print(f'Getting all second level urls... {url}')

    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(res.text, 'html.parser')

    bigBox = soup.find('ul', class_='woo-level-1')

    titles = bigBox.find_all('li', id='categoryname')

    second_lvl_urls = []

    for title in titles:
        url = title.find('a')['href']
        url = 'https://www.steelobrien.com' + url
        print(url)
        second_lvl_urls.append(url)
        time.sleep(2)

    return second_lvl_urls

def get_third_level_url(url):
    print(f'Getting all thrid level urls... {url}')

    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(res.text, 'html.parser')

    bigBox = soup.find('ul', class_='woo-level-1')

    titles = bigBox.find_all('li', id='categoryname')

    third_lvl_urls = []

    for title in titles:
        url = title.find('a')['href']
        url = 'https://www.steelobrien.com' + url
        print(url)
        third_lvl_urls.append(url)
        time.sleep(2)

    return third_lvl_urls

def get_forth_level_url(url):
    print(f'Getting all forth level urls... {url}')

    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(res.text, 'html.parser')

    bigBox = soup.find('ul', class_='woo-level-1')

    titles = bigBox.find_all('li', id='categoryname')

    forth_lvl_urls = []

    for title in titles:
        url = title.find('a')['href']
        url = 'https://www.steelobrien.com' + url
        print(url)
        forth_lvl_urls.append(url)
        time.sleep(2)

    return forth_lvl_urls

def get_detail(url):
    print(f'Getting detail... {url}')

    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    soup = BeautifulSoup(res.text, 'html.parser')

    breadcrumb = soup.find('nav', class_='woocommerce-breadcrumb').get_text(strip=True)

    list_bread = breadcrumb.split('>')
    print(list_bread)

    product_code = list_bread[5].split(' ')
    product_code = product_code[0]

    col2 = list_bread[3]
    col3 = list_bread[4]
    col4 = product_code
    col5 = list_bread[5] # product name

    dict_data = {
        'col1': 'New',
        'col2': col2,
        'col3': col3,
        'col4': col4,
        'col5': col5
    }

    with open(f'./results/{url.replace("/", "")}.json', 'w') as outfile:
        json.dump(dict_data, outfile)

def create_excel():
    files = sorted(glob.glob('./results/*.json'))

    datas = []
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
            datas.append(data)

    df = pd.DataFrame(datas)
    df.to_excel('result.xlsx')

    print('Excel ready...')

def run():

    while True:
        options = int(input('Number: '))

        if options == 1:
            total_page = check_url_status()

        if options == 2:
            total_urls = []
            urls = get_urls_all_item()
            total_urls += urls
            time.sleep(2)

            with open('all_urls.json', 'w') as outfile:
                json.dump(total_urls, outfile)

        if options == 3:

            with open('all_urls.json') as json_file:
                all_url = json.load(json_file)

            second_lvl_total = []
            for co, url in enumerate(all_url):
                print(co)
                try:
                    second_lvl = get_second_level_url(url)
                    second_lvl_total += second_lvl
                    time.sleep(3)
                except:
                    pass

                with open('all_second_level_urls.json', 'w') as outfile:
                    json.dump(second_lvl_total, outfile)

        if options == 4:

            with open('all_second_level_urls.json') as json_file:
                all_url = json.load(json_file)

            third_lvl_total = []

            for url in all_url:
                try:
                    third_lvl = get_third_level_url(url)
                    third_lvl_total += third_lvl
                    time.sleep(3)
                except:
                    pass

                with open('all_third_level_urls.json', 'w') as outfile:
                    json.dump(third_lvl_total, outfile)

        if options == 5:

            with open('all_third_level_urls.json') as json_file:
                all_url = json.load(json_file)

            four_lvl_total = []

            for url in all_url:
                try:
                    four_lvl = get_third_level_url(url)
                    four_lvl_total += four_lvl
                    time.sleep(3)
                except:
                    pass

                with open('all_four_level_urls.json', 'w') as outfile:
                    json.dump(four_lvl_total, outfile)

        if options == 6:
            with open('all_four_level_urls.json') as json_file:
                all_url = json.load(json_file)

            for url in all_url:
                get_detail(url)
                time.sleep(2)

        if options == 8:
            create_excel()

        if options == 9:
            break


if __name__ == '__main__':
    run()