import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import urllib3

urllib3.disable_warnings()
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}


def get_html(url, params=''):
    request = requests.get(url, verify=False, headers=HEADERS, params=params)
    return BeautifulSoup(request.text, 'html.parser')


def get_about(first_object):
    '''Находим описание лекарства'''
    link = first_object.find("div", class_="wrap-title-tn").find("a").get("href")
    soup = get_html(link)
    items_new = soup.find_all("div", class_="container")
    names = []  # все названия с сайта
    for j in items_new:
        title = j.find_all("span", class_="head")
        for h in title:
            names.append(h.text)
    output_data = []  # описание
    if 'Описание:' in names:
        data_about = soup.find("section", class_="ls-description general-section").find("span",
                                                                                        class_="value").get_text(
            strip=True)
        output_data.append(data_about)
    if 'Характеристика препарата:' in names:
        data_characteristic = soup.find("section", class_="ls-characteristics general-section").find("span",
                                                                                                     class_="value").get_text(
            strip=True)
        output_data.append(data_characteristic)
    if 'Лекарственная форма: \xa0' in names:
        data_form = soup.find("section", class_="ls-dosage-form general-section").find("span", class_="value").get_text(
            strip=True)
        output_data.append(data_form)
    if output_data:
        return output_data[0]
    return 'Описание продукта не удалось найти'


def get_analog(soup_main, product_url):
    '''Находим аналог лекарства'''
    link = soup_main.find('a', class_='collapse-synonims toogle-synonims')
    href = link.get('href')
    soup2 = get_html(urljoin(product_url, href))
    all_urls = set()
    sets = set()
    for i in soup2.find_all('a', class_="tn-vhodit-mnn-link"):
        url = i['href']
        all_urls.add(url)
        sets.add('-'.join(url.split('-')[:-1]))
    count = 0
    lst = list()
    for i in sets:
        if count == 5:
            break
        for j in all_urls:
            if i in j:
                s = get_html(j)
                text = s.find('span', class_="value").get_text(strip=True)
                text = ''.join((i for i in text if i.isalpha()))
                lst.append(text.capitalize())
                break
        count += 1
    if lst:
        return ', '.join(lst)
    return 'У данного лекарства нет аналогов'


def find_about_and_analog(s):
    main_url = "https://www.lsgeotar.ru/cgi-bin/mb4x?usr_data=search&SSr=07E70B06173FF&procX17=&fun_id=&rtm_value=&clientWidth=1519&scrollTop=0&http_x13rsv=usr_data%3Dsearch&SearchText=" + s
    main_soup = get_html(main_url)
    try:
        object_first = main_soup.find_all("div", class_="wrap-trade-sticker")[0]
        about = get_about(object_first)
    except:
        about = 'Описание продукта не удалось найти'
    try:
        object_first = main_soup.find_all("div", class_="wrap-trade-sticker")[0]
        link = object_first.find("div", class_="wrap-title-tn").find("a").get("href")
        soup_of_info = get_html(link)
        analog = get_analog(soup_of_info, link)
    except:
        analog = 'У данного лекарства нет аналогов'
    return analog, about
