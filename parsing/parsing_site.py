import requests
from bs4 import BeautifulSoup
import csv
import info_file
import pharmacies_db
import urllib3

urllib3.disable_warnings()


def get_html(link, params=''):
    request = requests.get(link, verify=False, headers=HEADERS, params=params)
    return BeautifulSoup(request.text, 'html.parser')


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

HOW_MANY_CATEGORIES = 3
with open('all_products3.csv', 'w', newline='', encoding='utf-8-sig') as file:
    pharmacies_db.start_session()
    writer = csv.writer(file, delimiter=';')
    url = 'https://megapteka.ru/naberezhnye-chelny/catalog/medikamenty-i-bady-42'
    soup = get_html(url)
    categories = soup.find_all('div', class_="category-block-elem")[:HOW_MANY_CATEGORIES]
    main_url = 'https://megapteka.ru/'
    for category in categories:
        new_url = main_url + category.find('a').get('href')
        soup_in_category = get_html(new_url)

        products = soup_in_category.find_all("div", class_="product__wrap")
        category_name = category.text
        for pr in products:
            super_new_url = main_url + pr.find("a").get("href")
            soup_in_product = get_html(super_new_url)
            items = soup_in_product.find_all('div', class_="card-item app-grid-card-item is_list_dosage")
            for item in items:
                url_url = main_url + item.find("a").get("href")
                try:
                    last_soup = get_html(url_url)
                    name_of_product = last_soup.find('div', class_='title').text.split('в Набережных Челнах')[0].strip()
                    if '\n' in name_of_product:
                        name_of_product = ' '.join(' '.join(name_of_product.split('\n')).split())
                    name_of_product = name_of_product.replace('№', 'номер')
                    image_of_product = last_soup.find('div', class_='image').find('img')['src']
                    if not image_of_product.startswith('https'):
                        image_of_product = 'https://sun6-21.userapi.com/s/v1/ig2/wKZJ3Fs7S5m-zvmOfMo0NfHH_qBME7aslMq9u5liNB_Am49pJwShku47FUClMbQORzCBjNQTn4zVnPaj_Hnr7-cU.jpg?size=799x799&quality=96&crop=200,0,799,799&ava=1'
                    price_of_product = last_soup.find('span', class_="price").text
                    from_what = category_name
                    analog, about = info_file.find_about_and_analog(name_of_product)
                    analog = analog.replace('№', 'номер')
                    about = about.replace('№', 'номер')
                    names = last_soup.find_all('div', class_="pickup__merchant")
                    cords = last_soup.find_all('div', class_="pickup__address")
                    pharmacies = {}
                    for ind in range(len(names)):
                        name = names[ind].text
                        cord = cords[ind].text
                        if '\u200b' in cord:
                            cord = ' '.join(' '.join(cord.split('\u200b')).split())
                        name = name.replace('№', 'номер')
                        cord = cord.replace('№', 'номер')
                        if pharmacies.get(name) is None:
                            pharmacies[name] = [cord]
                        else:
                            coordinates = pharmacies.get(name)
                            coordinates.append(cord)
                            pharmacies[name] = coordinates
                    for k, v in pharmacies.items():
                        for value in v:
                            pharmacies_db.add_pharmacy(k, value)
                    datas = [name_of_product, image_of_product, price_of_product, from_what, analog, about, pharmacies]
                    writer.writerow(datas)
                except Exception as ex:
                    print('error', url_url, ex)
    pharmacies_db.unique_db()
